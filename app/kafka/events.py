from datetime import datetime, timezone
from uuid import uuid4

from app.kafka.schemas import Event, EventType, NotePayload
from app.models.note import Note


def _build_note_payload(note: Note) -> NotePayload:
    """
    Converts a Note ORM model into a Kafka payload.
    """
    return NotePayload(
        note_id=note.id,
        title=note.title,
        content=note.content,
        created_by=note.created_by,
    )


def _build_event(note: Note, event_type: EventType) -> Event:
    """
    Creates a generic event envelope for a Note.
    """
    return Event(
        event_id=uuid4(),
        event_type=event_type,
        occurred_at=datetime.now(timezone.utc),
        payload=_build_note_payload(note),
    )


def build_note_created_event(note: Note) -> Event:
    """
    Creates a NOTE_CREATED event.
    """
    return _build_event(note, EventType.NOTE_CREATED)


def build_note_updated_event(note: Note) -> Event:
    """
    Creates a NOTE_UPDATED event.
    """
    return _build_event(note, EventType.NOTE_UPDATED)


def build_note_deleted_event(note: Note) -> Event:
    """
    Creates a NOTE_DELETED event.
    """
    return _build_event(note, EventType.NOTE_DELETED)