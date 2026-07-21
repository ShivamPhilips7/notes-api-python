import logging

from aiokafka import AIOKafkaProducer

from app.kafka.schemas import Event

logger = logging.getLogger(__name__)


class KafkaProducerService:
    """
    Responsible for publishing domain events to Kafka.
    """

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        client_id: str,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._client_id = client_id
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        """
        Creates and starts the Kafka producer.
        """
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            client_id=self._client_id,

            # Automatically serialize keys and values
            key_serializer=lambda key: str(key).encode("utf-8"),
            value_serializer=lambda event: event.model_dump_json().encode("utf-8"),

            # Reliability
            acks="all",
            enable_idempotence=True,

            # Compression
            compression_type="gzip",
        )

        await self._producer.start()

        logger.info(
            "Kafka producer started (bootstrap_servers=%s, topic=%s)",
            self._bootstrap_servers,
            self._topic,
        )

    async def stop(self) -> None:
        """
        Stops the Kafka producer gracefully.
        """
        if self._producer is not None:
            await self._producer.stop()
            logger.info("Kafka producer stopped.")

    async def publish(self, event: Event) -> None:
        """
        Publishes a domain event to Kafka.
        """
        if self._producer is None:
            raise RuntimeError("Kafka producer has not been started.")

        try:
            await self._producer.send_and_wait(
                topic=self._topic,
                key=event.payload.note_id,
                value=event,
            )

            logger.info(
                "Published event=%s event_id=%s note_id=%s topic=%s",
                event.event_type,
                event.event_id,
                event.payload.note_id,
                self._topic,
            )

        except Exception:
            logger.exception(
                "Failed to publish event=%s event_id=%s note_id=%s",
                event.event_type,
                event.event_id,
                event.payload.note_id,
            )
            raise