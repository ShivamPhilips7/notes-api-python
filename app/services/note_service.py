import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from app.kafka.events import (
    build_note_created_event,
    build_note_deleted_event,
    build_note_updated_event,
)
from app.kafka.producer import KafkaProducerService
from app.models.note import Note
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate

logger = logging.getLogger(__name__)


class NoteService:
    def __init__(
        self,
        repository: NoteRepository,
        kafka_producer: KafkaProducerService,
    ) -> None:
        self.repository = repository
        self.kafka_producer = kafka_producer

    async def get_all_notes(self):
        logger.info("Fetching all notes")
        return await self.repository.get_all_notes()

    async def get_note_by_id(self, note_id: UUID):
        logger.info("Fetching note with ID: %s", note_id)

        note = await self.repository.get_note_by_id(note_id)

        if note is None:
            logger.warning("Note with ID %s not found", note_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        return note

    async def create_note(
        self,
        request: NoteCreate,
        username: str,
    ):
        logger.info("Creating note for user: %s", username)

        note = Note(
            title=request.title,
            content=request.content,
            created_by=username,
            created_at=datetime.now(),
        )

        note = await self.repository.create_note(note)

        logger.info(
            "Publishing NOTE_CREATED event for note %s",
            note.id,
        )

        await self.kafka_producer.publish(
            build_note_created_event(note)
        )

        return note

    async def update_note(
        self,
        note_id: UUID,
        request: NoteUpdate,
    ):
        logger.info("Updating note with ID: %s", note_id)

        note = await self.get_note_by_id(note_id)

        note.title = request.title
        note.content = request.content

        note = await self.repository.update_note(note)

        logger.info(
            "Publishing NOTE_UPDATED event for note %s",
            note.id,
        )

        await self.kafka_producer.publish(
            build_note_updated_event(note)
        )

        return note

    async def delete_note(
        self,
        note_id: UUID,
    ):
        logger.info("Deleting note with ID: %s", note_id)

        note = await self.get_note_by_id(note_id)

        await self.repository.delete_note(note)

        logger.info(
            "Publishing NOTE_DELETED event for note %s",
            note.id,
        )

        await self.kafka_producer.publish(
            build_note_deleted_event(note)
        )