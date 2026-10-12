from app.schemas.room import RoomFilter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.room import Room, RoomImage


class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        filters: RoomFilter | None = None,
        hotel_id: int | None = None,
    ) -> list[Room]:
        query = select(Room).options(joinedload(Room.hotel), selectinload(Room.images))

        target_hotel_id = filters.hotel_id if filters and filters.hotel_id is not None else hotel_id
        if target_hotel_id is not None:
            query = query.where(Room.hotel_id == target_hotel_id)

        if filters:
            if filters.min_price is not None:
                query = query.where(Room.price >= filters.min_price)
            if filters.max_price is not None:
                query = query.where(Room.price <= filters.max_price)
            if filters.capacity is not None:
                query = query.where(Room.capacity >= filters.capacity)
            query = query.offset(filters.skip).limit(filters.limit)
        else:
            query = query.offset(0).limit(100)

        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_id(self, room_id: int) -> Room | None:
        query = select(Room).options(joinedload(Room.hotel), selectinload(Room.images)).where(Room.id == room_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Room:
        room = Room(**data)
        self.session.add(room)
        await self.session.commit()
        return await self.get_by_id(room.id)

    async def update(self, room: Room, data: dict) -> Room:
        for key, value in data.items():
            setattr(room, key, value)
        await self.session.commit()
        return await self.get_by_id(room.id)

    async def delete(self, room: Room) -> None:
        await self.session.delete(room)
        await self.session.commit()

    async def add_image(self, room_id: int, url: str, key: str) -> RoomImage:
        image = RoomImage(room_id=room_id, url=url, key=key)
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def get_image_by_id(self, image_id: int) -> RoomImage | None:
        return await self.session.get(RoomImage, image_id)

    async def delete_image(self, image: RoomImage) -> None:
        await self.session.delete(image)
        await self.session.commit()