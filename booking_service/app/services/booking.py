from datetime import date

from app.exceptions import (
    BookingNotFoundError,
    RoomNotAvailableError,
    RoomNotFoundError,
)
from app.models.booking import Booking
from app.repositories.booking import BookingRepository
from app.repositories.room import RoomRepository
from app.schemas.booking import BookingCreate, BookingUpdate

from app.rabbitmq import rabbit_client
from app.core.config import settings


class BookingService:
    def __init__(self, booking_repo: BookingRepository, room_repo: RoomRepository):
        self.booking_repo = booking_repo
        self.room_repo = room_repo

    async def get_all(self) -> list[Booking]:
        return await self.booking_repo.get_all()

    async def get_by_id(self, booking_id: int) -> Booking:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking with id {booking_id} not found")
        return booking

    async def is_room_available(
        self,
        room_id: int,
        check_in: date,
        check_out: date,
        exclude_booking_id: int | None = None,
    ) -> bool:
        return await self.booking_repo.is_room_available(
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            exclude_booking_id=exclude_booking_id,
        )

    async def create(self, booking_data: BookingCreate, user_id: int) -> Booking:
            room = await self.room_repo.get_by_id(booking_data.room_id)
            if not room:
                raise RoomNotFoundError(f"Room with id {booking_data.room_id} not found")

            is_available = await self.is_room_available(
                room_id=booking_data.room_id,
                check_in=booking_data.check_in,
                check_out=booking_data.check_out,
            )
            if not is_available:
                raise RoomNotAvailableError("Room is already booked for these dates")

            days = (booking_data.check_out - booking_data.check_in).days
            nights = max(1, days)
            total_price = nights * room.price

            data = booking_data.model_dump()
            data["user_id"] = user_id
            data["total_price"] = total_price

            booking = await self.booking_repo.create(data)

            event_data = {
                "booking_id": booking.id,
                "user_id": booking.user_id,
                "room_id": booking.room_id,
                "total_price": float(booking.total_price),
                "check_in": booking.check_in,
                "check_out": booking.check_out,
                "status": booking.status,
            }

            await rabbit_client.publish_event(
                routing_key=settings.BOOKING_CREATED_ROUTING_KEY,
                message_data=event_data,
            )

            return booking


    async def update_status(
        self, booking_id: int, status_data: BookingUpdate
    ) -> Booking:
        booking = await self.get_by_id(booking_id)

        data = status_data.model_dump(exclude_unset=True)
        return await self.booking_repo.update(booking, data)

    async def delete(self, booking_id: int) -> None:
        booking = await self.get_by_id(booking_id)

        await self.booking_repo.delete(booking)