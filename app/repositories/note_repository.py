import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note

logger = logging.getLogger(__name__)


class NoteRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_notes(self):
        logger.info("Fetching all notes from the database")
        result = await self.db.execute(select(Note))
        return result.scalars().all()

    async def get_note_by_id(self, note_id: UUID):
        logger.info(f"Fetching note with ID: {note_id}")
        result = await self.db.execute(
            select(Note).where(Note.id == note_id)
        )
        return result.scalar_one_or_none()

    async def create_note(self, note: Note):
        logger.info(f"Creating note: {note.title}")
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def update_note(self, note: Note):
        logger.info(f"Updating note: {note.title}")
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def delete_note(self, note: Note):
        logger.info(f"Deleting note: {note.title}")
        await self.db.delete(note)
        await self.db.commit()