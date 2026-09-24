from fastapi import APIRouter, status

from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.api.dependencies import RoomServiceDep


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("", response_model=list[RoomResponse])
async def get_rooms(
    room_service: RoomServiceDep,
):
    return await room_service.get_all()


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room_by_id(
    room_id: int,
    room_service: RoomServiceDep,
):
    return await room_service.get_by_id(room_id)


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreate,
    room_service: RoomServiceDep,
):
    return await room_service.create(room_data)


@router.patch("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    room_data: RoomUpdate,
    room_service: RoomServiceDep,
):
    return await room_service.update(room_id, room_data)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    room_service: RoomServiceDep,
):
    await room_service.delete(room_id)