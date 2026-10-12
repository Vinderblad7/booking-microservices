from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.hotel import Hotel, HotelImage
from app.schemas.hotel import HotelFilter


class HotelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, filters: HotelFilter | None = None) -> list[Hotel]:
        query = select(Hotel).options(selectinload(Hotel.images))
        if filters:
            if filters.query:
                pattern = f"%{filters.query}%"
                query = query.where(
                    or_(
                        Hotel.name.ilike(pattern),
                        Hotel.description.ilike(pattern),
                    )
                )
            query = query.offset(filters.skip).limit(filters.limit)
        else:
            query = query.offset(0).limit(100)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, hotel_id: int) -> Hotel | None:
        query = select(Hotel).options(selectinload(Hotel.images)).where(Hotel.id == hotel_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Hotel | None:
        query = select(Hotel).options(selectinload(Hotel.images)).where(Hotel.slug == slug)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Hotel:
        hotel = Hotel(**data)
        self.session.add(hotel)
        await self.session.commit()
        return await self.get_by_id(hotel.id)

    async def update(self, hotel: Hotel, data: dict) -> Hotel:
        for key, value in data.items():
            setattr(hotel, key, value)
        await self.session.commit()
        return await self.get_by_id(hotel.id)

    async def delete(self, hotel: Hotel) -> None:
        await self.session.delete(hotel)
        await self.session.commit()

    async def add_image(self, hotel_id: int, url: str, key: str) -> HotelImage:
        image = HotelImage(hotel_id=hotel_id, url=url, key=key)
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def get_image_by_id(self, image_id: int) -> HotelImage | None:
        return await self.session.get(HotelImage, image_id)

    async def delete_image(self, image: HotelImage) -> None:
        await self.session.delete(image)
        await self.session.commit()