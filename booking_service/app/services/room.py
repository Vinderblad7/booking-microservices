from app.core.cache import cache
from app.exceptions import HotelNotFoundError, RoomNotFoundError
from app.redis import redis_client
from app.repositories.hotel import HotelRepository
from app.repositories.room import RoomRepository
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate


class RoomService:
    def __init__(self, room_repo: RoomRepository, hotel_repo: HotelRepository):
        self.room_repo = room_repo
        self.hotel_repo = hotel_repo

    @cache(expire=300, prefix="rooms:all")
    async def get_all(self) -> list[RoomResponse]:
        rooms = await self.room_repo.get_all()
        return [RoomResponse.model_validate(r) for r in rooms]

    @cache(expire=300, prefix="rooms:id")
    async def get_by_id(self, room_id: int) -> RoomResponse:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError(f"Room with id {room_id} not found")
        return RoomResponse.model_validate(room)

    async def create(self, data: RoomCreate) -> RoomResponse:
        hotel_exist = await self.hotel_repo.get_by_id(data.hotel_id)
        if not hotel_exist:
            raise HotelNotFoundError(f"Hotel with id {data.hotel_id} not found")

        created_room = await self.room_repo.create(data.model_dump())

        await redis_client.delete_by_pattern("rooms:*")

        return RoomResponse.model_validate(created_room)

    async def update(self, room_id: int, room_data: RoomUpdate) -> RoomResponse:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError(f"Room with id {room_id} not found")

        data = room_data.model_dump(exclude_unset=True)

        updated_room = await self.room_repo.update(room, data)

        await redis_client.delete_by_pattern("rooms:*")

        return RoomResponse.model_validate(updated_room)

    async def delete(self, room_id: int) -> None:
        room = await self.room_repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError(f"Room with id {room_id} not found")

        await self.room_repo.delete(room)

        await redis_client.delete_by_pattern("rooms:*")