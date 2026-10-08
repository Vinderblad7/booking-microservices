from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.dependencies import SessionDep
from app.exceptions import InvalidTokenError
from app.repositories.booking import BookingRepository
from app.repositories.hotel import HotelRepository
from app.repositories.room import RoomRepository
from app.services.booking import BookingService
from app.services.hotel import HotelService
from app.services.room import RoomService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


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


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise InvalidTokenError("Invalid or expired access token")

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenError("Token subject is missing")

    return int(user_id_str)


HotelServiceDep = Annotated[HotelService, Depends(get_hotel_service)]
RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]
BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]