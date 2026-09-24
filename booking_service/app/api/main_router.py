from fastapi import APIRouter

from app.api.booking import router as bookings_router
from app.api.hotel import router as hotels_router
from app.api.room import router as rooms_router

main_router = APIRouter(prefix="/api")

main_router.include_router(hotels_router)
main_router.include_router(rooms_router)
main_router.include_router(bookings_router)