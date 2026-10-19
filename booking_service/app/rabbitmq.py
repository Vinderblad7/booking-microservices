import json
from typing import Any
import aio_pika
from aio_pika import ExchangeType, Message, RobustChannel, RobustConnection

from app.core.config import settings
from app.core.database import new_session


class RabbitMQClient:
    def __init__(self) -> None:
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None
        self.exchange: aio_pika.RobustExchange | None = None
        self.payment_exchange: aio_pika.RobustExchange | None = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()

        self.exchange = await self.channel.declare_exchange(
            name=settings.BOOKING_EXCHANGE,
            type=ExchangeType.TOPIC,
            durable=True,
        )

        self.payment_exchange = await self.channel.declare_exchange(
            name=settings.PAYMENT_EXCHANGE,
            type=ExchangeType.TOPIC,
            durable=True,
        )

    async def close(self) -> None:
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    async def publish_event(self, routing_key: str, message_data: dict[str, Any]) -> None:
        if not self.exchange:
            raise RuntimeError("RabbitMQ exchange is not initialized. Call connect() first.")

        body = json.dumps(message_data, default=str).encode("utf-8")

        message = Message(
            body=body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await self.exchange.publish(message, routing_key=routing_key)

    async def consume_payment_events(self) -> None:
        if not self.channel or not self.payment_exchange:
            raise RuntimeError(
                "RabbitMQ channel or exchange is not initialized. Call connect() first."
            )

        queue = await self.channel.declare_queue(name="booking_payment_queue", durable=True)
        await queue.bind(exchange=self.payment_exchange, routing_key="payment.#")

        from app.models.booking import BookingStatus
        from app.repositories.booking import BookingRepository
        from app.repositories.room import RoomRepository
        from app.schemas.booking import BookingUpdate
        from app.services.booking import BookingService

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode("utf-8"))
                    booking_id = int(payload["booking_id"])
                    payment_status = payload.get("status")

                    async with new_session() as session:
                        booking_repo = BookingRepository(session)
                        room_repo = RoomRepository(session)
                        booking_service = BookingService(booking_repo, room_repo)

                        if payment_status == "success":
                            new_status = BookingStatus.PAID
                        else:
                            new_status = BookingStatus.CANCELLED

                        await booking_service.update_status(
                            booking_id, status_data=BookingUpdate(status=new_status)
                        )


rabbit_client = RabbitMQClient()