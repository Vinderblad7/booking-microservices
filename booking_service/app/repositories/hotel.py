from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Hotel


class HotelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Hotel]:
        query = select(Hotel).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, hotel_id: int) -> Hotel | None:
        return await self.session.get(Hotel, hotel_id)

    async def get_by_slug(self, slug: str) -> Hotel | None:
        query = select(Hotel).where(Hotel.slug == slug)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create(self, data: dict) -> Hotel:
        hotel = Hotel(**data)
        self.session.add(hotel)
        await self.session.commit()
        await self.session.refresh(hotel)
        return hotel

    async def update(self, hotel: Hotel, data: dict) -> Hotel:
        for key, value in data.items():
            setattr(hotel, key, value)
        await self.session.commit()
        await self.session.refresh(hotel)
        return hotel

    async def delete(self, hotel: Hotel) -> None:
        await self.session.delete(hotel)
        await self.session.commit()