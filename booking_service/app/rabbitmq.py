import json
from typing import Any
import aio_pika
from aio_pika import ExchangeType, Message, RobustChannel, RobustConnection

from app.core.config import settings


class RabbitMQClient:
    def __init__(self) -> None:
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None
        self.exchange: aio_pika.RobustExchange | None = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        
        self.exchange = await self.channel.declare_exchange(
            name=settings.BOOKING_EXCHANGE,
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


rabbit_client = RabbitMQClient()