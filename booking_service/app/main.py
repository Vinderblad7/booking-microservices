from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.main_router import main_router

app = FastAPI(
    title="Booking Service API",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(main_router)


@app.get("/health", tags=["Healthcheck"])
async def healthcheck():
    return {"status": "ok"}