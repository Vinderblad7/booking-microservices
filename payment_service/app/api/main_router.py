from fastapi import APIRouter

from app.api.payment import router as payments_router

main_router = APIRouter(prefix="/api")

main_router.include_router(payments_router)
