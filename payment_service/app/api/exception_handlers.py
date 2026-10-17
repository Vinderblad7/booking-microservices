from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    InvalidTokenError,
    PaymentAlreadyExistsError,
    PaymentAlreadyProcessedError,
    PaymentFailedError,
    PaymentNotFoundError,
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


async def bad_request_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def unauthorized_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PaymentNotFoundError, not_found_handler)
    app.add_exception_handler(PaymentAlreadyExistsError, conflict_handler)
    app.add_exception_handler(PaymentAlreadyProcessedError, conflict_handler)
    app.add_exception_handler(PaymentFailedError, bad_request_handler)
    app.add_exception_handler(InvalidTokenError, unauthorized_handler)
