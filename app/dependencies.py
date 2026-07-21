from fastapi import Depends
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.kafka.producer import KafkaProducerService
from app.config.database import get_db
from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.note_service import NoteService
from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.security.jwt_handler import (
    decode_access_token,
    oauth2_scheme,
)

def get_kafka_producer(
    request: Request,
) -> KafkaProducerService:
    """
    Returns the application-wide Kafka producer.
    """
    return request.app.state.kafka_producer

def get_note_repository(
    db: AsyncSession = Depends(get_db),
) -> NoteRepository:
    return NoteRepository(db)


def get_note_service(
    repository: NoteRepository = Depends(get_note_repository),
    kafka_producer: KafkaProducerService = Depends(get_kafka_producer),
) -> NoteService:
    return NoteService(repository, kafka_producer)


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repository)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(get_user_repository),
) -> User:

    payload = decode_access_token(token)

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await repository.get_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user