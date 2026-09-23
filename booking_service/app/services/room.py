from app.repositories.room import RoomRepository
from app.repositories.hotel import HotelRepository
from app.schemas.room import RoomCreate, RoomUpdate
from app.models.room import Room
from app.exceptions import RoomNotFoundError, HotelNotFoundError

class RoomService:
    def __init__(self, room_repo: RoomRepository, hotel_repo: HotelRepository):
        self.room_repo = room_repo
        self.hotel_repo = hotel_repo

    async def get_all(self) -> list[Room]:
        return await self.room_repo.get_all()

    async def get_by_id(self, room_id: int) -> Room:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError(f"Room with id {room_id} not found")
        return room

    async def create(self, data: RoomCreate) -> Room:
        hotel_exist = await self.hotel_repo.get_by_id(data.hotel_id)
        if not hotel_exist:
            raise HotelNotFoundError(f"Hotel with id {data.hotel_id} not found")

        return await self.room_repo.create(data.model_dump())

    async def update(self, room_id: int, room_data: RoomUpdate) -> Room:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError(f"Room with id {room_id} not found")

        data = room_data.model_dump(exclude_unset=True)

        return await self.room_repo.update(room_id, data)

    async def delete(self, room_id: int) -> None:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError(f"Room with id {room_id} not found")

        await self.room_repo.delete(room_id)