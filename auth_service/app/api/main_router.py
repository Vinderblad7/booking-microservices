from fastapi import APIRouter

from app.api.auth import router as auth_router

main_router = APIRouter(prefix="/api")

main_router.include_router(auth_router)
