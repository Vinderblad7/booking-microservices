import asyncio
from decimal import Decimal
import json
from typing import Any

import aio_pika
from aio_pika import ExchangeType, Message, RobustChannel, RobustConnection, RobustExchange

from app.core.config import settings
from app.core.database import new_session
from app.models.payment import PaymentStatus
from app.repositories.payment import PaymentRepository
from app.schemas.payment import PaymentCreate
from app.services.payment import PaymentService


class RabbitMQClient:
    def __init__(self) -> None:
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None
        self.payment_exchange: RobustExchange | None = None
        self.booking_exchange: RobustExchange | None = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()

        self.payment_exchange = await self.channel.declare_exchange(
            name=settings.PAYMENT_EXCHANGE,
            type=ExchangeType.TOPIC,
            durable=True,
        )

        self.booking_exchange = await self.channel.declare_exchange(
            name=settings.BOOKING_EXCHANGE,
            type=ExchangeType.TOPIC,
            durable=True,
        )

    async def close(self) -> None:
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def publish_event(
        self, routing_key: str, message_data: dict[str, Any]
    ) -> None:
        if not self.payment_exchange:
            raise RuntimeError(
                "Payment exchange is not initialized. Call connect() first."
            )

        body = json.dumps(message_data, default=str).encode("utf-8")

        message = Message(
            body=body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.payment_exchange.publish(message, routing_key=routing_key)

    async def consume_booking_events(self) -> None:
        if not self.channel or not self.booking_exchange:
            raise RuntimeError(
                "RabbitMQ channel or exchange is not initialized. Call connect() first."
            )

        queue = await self.channel.declare_queue(
            name="payment_booking_queue",
            durable=True,
        )

        await queue.bind(
            self.booking_exchange,
            routing_key=settings.BOOKING_CREATED_ROUTING_KEY,
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode("utf-8"))

                    booking_id = int(payload["booking_id"])
                    user_id = int(payload["user_id"])
                    amount = Decimal(str(payload["total_price"]))

                    async with new_session() as session:
                        payment_repo = PaymentRepository(session)
                        payment_service = PaymentService(payment_repo)

                        payment_create = PaymentCreate(
                            booking_id=booking_id,
                            amount=amount,
                        )

                        payment = await payment_service.create(
                            user_id=user_id,
                            data=payment_create,
                        )

                        payment = await payment_service.process_payment(
                            payment_id=payment.id
                        )

                        routing_key = (
                            settings.PAYMENT_SUCCESS_ROUTING_KEY
                            if payment.status == PaymentStatus.SUCCESS
                            else settings.PAYMENT_FAILED_ROUTING_KEY
                        )

                        event_data = {
                            "payment_id": payment.id,
                            "booking_id": payment.booking_id,
                            "user_id": payment.user_id,
                            "amount": float(payment.amount),
                            "status": payment.status.value,
                        }

                        await self.publish_event(
                            routing_key=routing_key,
                            message_data=event_data,
                        )


rabbit_client = RabbitMQClient()
