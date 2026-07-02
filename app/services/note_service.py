import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from app.models.note import Note
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate

logger = logging.getLogger(__name__)

class NoteService:

    def __init__(self, repository: NoteRepository):
        self.repository = repository

    async def get_all_notes(self):
        logger.info("Fetching all notes")
        return await self.repository.get_all_notes()

    async def get_note_by_id(self, note_id: UUID):
        logger.info(f"Fetching note with ID: {note_id}")
        note = await self.repository.get_note_by_id(note_id)

        if note is None:
            logger.warning(f"Note with ID {note_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        return note

    async def create_note(self, request: NoteCreate, username: str):
        logger.info(f"Creating note for user: {username}")
        note = Note(
            title=request.title,
            content=request.content,
            created_by=username,
            created_at=datetime.now(),
        )

        return await self.repository.create_note(note)

    async def update_note(
        self,
        note_id: UUID,
        request: NoteUpdate,
    ):
        logger.info(f"Updating note with ID: {note_id}")
        note = await self.get_note_by_id(note_id)

        note.title = request.title
        note.content = request.content

        return await self.repository.update_note(note)

    async def delete_note(self, note_id: UUID):
        logger.info(f"Deleting note with ID: {note_id}")
        note = await self.get_note_by_id(note_id)

        await self.repository.delete_note(note)