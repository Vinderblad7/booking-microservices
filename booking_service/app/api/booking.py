from datetime import date
from fastapi import APIRouter, status, Query

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingUpdate,
)
from app.api.dependencies import BookingServiceDep


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=list[BookingResponse])
async def get_bookings(
    booking_service: BookingServiceDep,
):
    return await booking_service.get_all()


@router.get("/check-availability", response_model=bool)
async def check_room_availability(
    room_id: int,
    check_in: date,
    check_out: date,
    booking_service: BookingServiceDep,
    exclude_booking_id: int | None = Query(default=None),
):
    return await booking_service.is_room_available(
        room_id=room_id,
        check_in=check_in,
        check_out=check_out,
        exclude_booking_id=exclude_booking_id,
    )


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking_by_id(
    booking_id: int,
    booking_service: BookingServiceDep,
):
    return await booking_service.get_by_id(booking_id)


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    booking_service: BookingServiceDep,
    user_id: int = Query(..., description="user ID"),
):
    return await booking_service.create(booking_data=booking_data, user_id=user_id)


@router.patch("/{booking_id}/status", response_model=BookingResponse)
async def update_booking_status(
    booking_id: int,
    status_data: BookingUpdate,
    booking_service: BookingServiceDep,
):
    return await booking_service.update_status(
        booking_id=booking_id, status_data=status_data
    )


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    booking_service: BookingServiceDep,
):
    await booking_service.delete(booking_id)