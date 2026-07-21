from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventType(str, Enum):
    NOTE_CREATED = "NOTE_CREATED"
    NOTE_UPDATED = "NOTE_UPDATED"
    NOTE_DELETED = "NOTE_DELETED"


class NotePayload(BaseModel):
    note_id: UUID
    title: str
    content: str
    created_by: str


class Event(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True
    )

    event_id: UUID
    event_type: EventType
    event_version: int = 1
    occurred_at: datetime
    payload: NotePayload