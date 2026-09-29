from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.exception_handlers import register_exception_handlers
from app.api.main_router import main_router

from app.rabbitmq import rabbit_client
from app.redis import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_client.connect()
    await redis_client.connect()
    yield
    await redis_client.close()
    await rabbit_client.close()

app = FastAPI(
    title="Booking Service API",
    version="1.0.0",
    lifespan=lifespan
)

register_exception_handlers(app)

app.include_router(main_router)


@app.get("/health", tags=["Healthcheck"])
async def healthcheck():
    return {"status": "ok"}