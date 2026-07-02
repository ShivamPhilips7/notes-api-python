from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: UUID
    title: str
    content: str
    created_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)