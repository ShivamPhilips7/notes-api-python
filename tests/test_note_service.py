from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.note_service import NoteService


@pytest.mark.asyncio
async def test_get_all_notes(mock_note_repository, mock_kafka_producer):
    """
    Test retrieving all notes.
    """

    notes = [
        Note(
            title="Note 1",
            content="Content 1",
            created_by="ash",
            created_at=datetime.now(),
        ),
        Note(
            title="Note 2",
            content="Content 2",
            created_by="ash",
            created_at=datetime.now(),
        ),
    ]

    mock_note_repository.get_all_notes.return_value = notes

    service = NoteService(mock_note_repository, mock_kafka_producer)

    result = await service.get_all_notes()

    assert len(result) == 2
    mock_note_repository.get_all_notes.assert_called_once()
    mock_kafka_producer.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_note_by_id(mock_note_repository, mock_kafka_producer):
    """
    Test retrieving a note by ID.
    """

    note_id = uuid4()

    note = Note(
        id=note_id,
        title="Test Note",
        content="Test Content",
        created_by="ash",
        created_at=datetime.now(),
    )

    mock_note_repository.get_note_by_id.return_value = note

    service = NoteService(mock_note_repository, mock_kafka_producer)

    result = await service.get_note_by_id(note_id)

    assert result.id == note_id
    assert result.title == "Test Note"

    mock_note_repository.get_note_by_id.assert_called_once_with(note_id)
    mock_kafka_producer.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_note_by_id_not_found(mock_note_repository, mock_kafka_producer):
    """
    Test retrieving a non-existent note.
    """

    note_id = uuid4()

    mock_note_repository.get_note_by_id.return_value = None

    service = NoteService(mock_note_repository, mock_kafka_producer)

    with pytest.raises(HTTPException) as exc:
        await service.get_note_by_id(note_id)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Note not found"
    mock_kafka_producer.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_note(mock_note_repository, mock_kafka_producer):
    """
    Test creating a note.
    """

    request = NoteCreate(
        title="Meeting",
        content="Discuss FastAPI"
    )

    created_note = Note(
        id=uuid4(),
        title=request.title,
        content=request.content,
        created_by="ash",
        created_at=datetime.now(),
    )

    mock_note_repository.create_note.return_value = created_note

    service = NoteService(mock_note_repository, mock_kafka_producer)

    result = await service.create_note(
        request,
        "ash",
    )

    assert result.title == "Meeting"
    assert result.created_by == "ash"

    mock_note_repository.create_note.assert_called_once()

    saved_note = mock_note_repository.create_note.call_args.args[0]

    assert saved_note.title == "Meeting"
    assert saved_note.content == "Discuss FastAPI"
    assert saved_note.created_by == "ash"

    mock_kafka_producer.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_note(mock_note_repository, mock_kafka_producer):
    """
    Test updating a note.
    """

    note_id = uuid4()

    note = Note(
        id=note_id,
        title="Old Title",
        content="Old Content",
        created_by="ash",
        created_at=datetime.now(),
    )

    mock_note_repository.get_note_by_id.return_value = note
    mock_note_repository.update_note.return_value = note

    service = NoteService(mock_note_repository, mock_kafka_producer)

    request = NoteUpdate(
        title="New Title",
        content="New Content",
    )

    result = await service.update_note(
        note_id,
        request,
    )

    assert result.title == "New Title"
    assert result.content == "New Content"

    mock_note_repository.update_note.assert_called_once_with(note)
    mock_kafka_producer.publish.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_note(mock_note_repository, mock_kafka_producer):
    """
    Test deleting a note.
    """

    note_id = uuid4()

    note = Note(
        id=note_id,
        title="Delete Me",
        content="Delete Content",
        created_by="ash",
        created_at=datetime.now(),
    )

    mock_note_repository.get_note_by_id.return_value = note

    service = NoteService(mock_note_repository, mock_kafka_producer)

    await service.delete_note(note_id)

    mock_note_repository.delete_note.assert_called_once_with(note)
    mock_kafka_producer.publish.assert_awaited_once()