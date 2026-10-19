from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import register_exception_handlers
from app.api.main_router import main_router
from app.core.config import settings
from app.core.database import new_session
from app.core.security import hash_password
from app.models.user import UserRole
from app.repositories.user import UserRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with new_session() as session:
        user_repo = UserRepository(session)
        existing = await user_repo.get_by_email(settings.FIRST_SUPERUSER_EMAIL)
        if not existing:
            await user_repo.create(
                {
                    "email": settings.FIRST_SUPERUSER_EMAIL,
                    "hashed_password": hash_password(settings.FIRST_SUPERUSER_PASSWORD),
                    "role": UserRole.ADMIN,
                    "is_active": True,
                }
            )
    yield


app = FastAPI(
    title="Auth Service API",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(main_router)


@app.get("/health", tags=["Healthcheck"])
async def healthcheck():
    return {"status": "ok"}
