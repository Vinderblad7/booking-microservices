from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        user_id: int | None = None,
        booking_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        query = select(Payment)

        if user_id is not None:
            query = query.where(Payment.user_id == user_id)
        if booking_id is not None:
            query = query.where(Payment.booking_id == booking_id)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)

        return list(result.scalars().unique().all())

    async def get_by_id(self, payment_id: int) -> Payment | None:
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_booking_id(self, booking_id: int) -> Payment | None:
        query = select(Payment).where(Payment.booking_id == booking_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Payment:
        payment = Payment(**data)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def update(self, payment: Payment, data: dict) -> Payment:
        for key, value in data.items():
            setattr(payment, key, value)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment