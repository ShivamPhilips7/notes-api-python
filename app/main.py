import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.logging_config import setup_logging
from app.config.settings import settings
from app.exceptions import register_exception_handlers
from app.kafka.producer import KafkaProducerService
from app.routers.auth_router import router as auth_router
from app.routers.health_router import router as health_router
from app.routers.note_router import router as note_router

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown resources.
    """

    logger.info("Starting Notes API...")

    kafka_producer = KafkaProducerService(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        topic=settings.KAFKA_TOPIC,
        client_id=settings.KAFKA_CLIENT_ID,
    )

    await kafka_producer.start()

    app.state.kafka_producer = kafka_producer

    logger.info("Kafka producer initialized.")

    try:
        yield
    finally:
        await kafka_producer.stop()
        logger.info("Kafka producer stopped.")


app = FastAPI(
    title="Notes API",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(note_router)
app.include_router(health_router)


@app.get("/")
async def home():
    return {
        "message": "Notes API is running"
    }