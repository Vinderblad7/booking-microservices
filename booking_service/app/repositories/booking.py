from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.booking import Booking, BookingStatus


class BookingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        user_id: int | None = None,
        room_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Booking]:
        query = select(Booking).options(joinedload(Booking.room))

        if user_id is not None:
            query = query.where(Booking.user_id == user_id)
        if room_id is not None:
            query = query.where(Booking.room_id == room_id)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_id(self, booking_id: int) -> Booking | None:
        query = (
            select(Booking)
            .options(joinedload(Booking.room))
            .where(Booking.id == booking_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def is_room_available(
        self,
        room_id: int,
        check_in: date,
        check_out: date,
        exclude_booking_id: int | None = None,
    ) -> bool:
        
        query = select(Booking).where(
            Booking.room_id == room_id,
            Booking.status != BookingStatus.CANCELLED,
            and_(
                Booking.check_in < check_out,
                Booking.check_out > check_in,
            ),
        )

        if exclude_booking_id is not None:
            query = query.where(Booking.id != exclude_booking_id)

        result = await self.session.execute(query)
        return result.scalar_one_or_none() is None

    async def create(self, data: dict) -> Booking:
        booking = Booking(**data)
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def update(self, booking: Booking, data: dict) -> Booking:
        for key, value in data.items():
            setattr(booking, key, value)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def delete(self, booking: Booking) -> None:
        await self.session.delete(booking)
        await self.session.commit()