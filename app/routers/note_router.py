import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies import get_note_service
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.security.roles import require_role
from app.services.note_service import NoteService
from app.dependencies import (
    get_current_user,
    get_note_service,
)

from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.get("", response_model=list[NoteResponse])
async def get_all_notes(
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    logger.info(f"Fetching all notes for user: {current_user.username}")
    return await service.get_all_notes()


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note_by_id(
    note_id: UUID,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    logger.info(f"Fetching note by ID: {note_id}")
    return await service.get_note_by_id(note_id)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    request: NoteCreate,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    logger.info(f"Creating note for user: {current_user.username}")
    return await service.create_note(request, current_user.username)


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
)
async def update_note(
    note_id: UUID,
    request: NoteUpdate,
    current_user: User = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    logger.info(f"Updating note: {note_id}")
    return await service.update_note(note_id, request)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: UUID,
    current_user: User = Depends(require_role("ADMIN")),
    service: NoteService = Depends(get_note_service),
):
    logger.info(f"Deleting note: {note_id}")
    await service.delete_note(note_id)
