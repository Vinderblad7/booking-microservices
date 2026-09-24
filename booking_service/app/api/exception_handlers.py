from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    BookingNotFoundError,
    HotelAlreadyExistsError,
    HotelNotFoundError,
    RoomNotAvailableError,
    RoomNotFoundError,
)


async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


async def conflict_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HotelNotFoundError, not_found_handler)
    app.add_exception_handler(RoomNotFoundError, not_found_handler)
    app.add_exception_handler(BookingNotFoundError, not_found_handler)

    app.add_exception_handler(HotelAlreadyExistsError, conflict_handler)
    app.add_exception_handler(RoomNotAvailableError, conflict_handler)