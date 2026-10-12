from fastapi import APIRouter, Depends, UploadFile, status

from app.api.dependencies import RoomServiceDep
from app.schemas.room import (
    RoomCreate,
    RoomFilter,
    RoomImageResponse,
    RoomResponse,
    RoomUpdate,
)

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("", response_model=list[RoomResponse])
async def get_rooms(
    room_service: RoomServiceDep,
    filters: RoomFilter = Depends(),
):
    return await room_service.get_all(filters)


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


@router.post(
    "/{room_id}/images",
    response_model=RoomImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_room_image(
    room_id: int,
    file: UploadFile,
    room_service: RoomServiceDep,
):
    return await room_service.upload_image(room_id, file)


@router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_room_image(
    image_id: int,
    room_service: RoomServiceDep,
):
    await room_service.delete_image(image_id)