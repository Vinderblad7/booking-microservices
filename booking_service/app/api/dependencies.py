from typing import Annotated
from fastapi import Depends
from app.dependencies import SessionDep

from app.repositories.hotel import HotelRepository
from app.repositories.room import RoomRepository
from app.repositories.booking import BookingRepository

from app.services.hotel import HotelService
from app.services.room import RoomService
from app.services.booking import BookingService


async def get_hotel_service(session: SessionDep) -> HotelService:
    hotel_repo = HotelRepository(session)
    return HotelService(hotel_repo)


async def get_room_service(session: SessionDep) -> RoomService:
    room_repo = RoomRepository(session)
    hotel_repo = HotelRepository(session)
    return RoomService(room_repo=room_repo, hotel_repo=hotel_repo)


async def get_booking_service(session: SessionDep) -> BookingService:
    booking_repo = BookingRepository(session)
    room_repo = RoomRepository(session)
    return BookingService(booking_repo=booking_repo, room_repo=room_repo)


HotelServiceDep = Annotated[HotelService, Depends(get_hotel_service)]
RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]
BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]