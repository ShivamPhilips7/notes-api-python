import logging
from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.note_router import router as note_router
from app.routers.health_router import router as health_router
from app.config.logging_config import setup_logging
from app.exceptions import register_exception_handlers

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notes API",
    version="1.0.0",
)

register_exception_handlers(app)

logger.info("Starting Notes API...")

app.include_router(auth_router)
app.include_router(note_router)
app.include_router(health_router)

@app.get("/")
async def home():
    return {
        "message": "Notes API is running"
    }