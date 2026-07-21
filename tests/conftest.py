import pytest
from unittest.mock import AsyncMock

from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserRepository
from app.kafka.producer import KafkaProducerService


@pytest.fixture
def mock_user_repository():
    """
    Mock UserRepository for AuthService tests.
    """
    repository = AsyncMock(spec=UserRepository)

    repository.get_by_username = AsyncMock()
    repository.get_by_email = AsyncMock()
    repository.create_user = AsyncMock()

    return repository


@pytest.fixture
def mock_note_repository():
    """
    Mock NoteRepository for NoteService tests.
    """
    repository = AsyncMock(spec=NoteRepository)

    repository.get_all_notes = AsyncMock()
    repository.get_note_by_id = AsyncMock()
    repository.create_note = AsyncMock()
    repository.update_note = AsyncMock()
    repository.delete_note = AsyncMock()

    return repository

@pytest.fixture
def mock_kafka_producer():
    """
    Mock KafkaProducerService for NoteService tests.
    """
    producer = AsyncMock(spec=KafkaProducerService)

    producer.publish = AsyncMock()

    return producer