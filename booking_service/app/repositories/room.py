from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.room import Room


class RoomRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self, hotel_id: int | None = None, skip: int = 0, limit: int = 100
    ) -> list[Room]:
        query = select(Room).options(joinedload(Room.hotel))
        if hotel_id is not None:
            query = query.where(Room.hotel_id == hotel_id)
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_id(self, room_id: int) -> Room | None:
        query = select(Room).options(joinedload(Room.hotel)).where(Room.id == room_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Room:
        room = Room(**data)
        self.session.add(room)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def update(self, room: Room, data: dict) -> Room:
        for key, value in data.items():
            setattr(room, key, value)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def delete(self, room: Room) -> None:
        await self.session.delete(room)
        await self.session.commit()