from datetime import date
from app.repositories.booking import BookingRepository
from app.repositories.room import RoomRepository
from app.schemas.booking import BookingCreate, BookingStatusUpdate
from app.models.booking import Booking
from app.exceptions import (
    BookingNotFoundError,
    RoomNotFoundError,
    RoomNotAvailableError,
)

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

        nights = (booking_data.check_out - booking_data.check_in).days
        total_price = nights * room.price

        data = booking_data.model_dump()
        data["user_id"] = user_id
        data["total_price"] = total_price

        return await self.booking_repo.create(data)

    async def update_status(self, booking_id: int, status_data: BookingStatusUpdate) -> Booking:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking with id {booking_id} not found")

        data = status_data.model_dump(exclude_unset=True)
        return await self.booking_repo.update(booking_id, data)

    async def delete(self, booking_id: int) -> None:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise BookingNotFoundError(f"Booking with id {booking_id} not found")

        await self.booking_repo.delete(booking_id)