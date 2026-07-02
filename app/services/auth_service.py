import logging
from datetime import datetime,timezone

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token, UserRegister
from app.security.jwt_handler import create_access_token
from app.security.password import (
    hash_password,
    verify_password,
)

logger = logging.getLogger(__name__)

class AuthService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def register(
        self,
        request: UserRegister,
    ):
        logger.info(f"Registering user: {request.username}")

        existing_username = await self.repository.get_by_username(
            request.username
        )

        if existing_username:
            logger.warning(f"Username {request.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

        existing_email = await self.repository.get_by_email(
            request.email
        )

        if existing_email:
            logger.warning(f"Email {request.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        user = User(
            username=request.username,
            email=request.email,
            password=hash_password(request.password),
            created_at=datetime.now(),
        )

        return await self.repository.create_user(user)

    async def authenticate(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> Token:
        logger.info(f"Authenticating user: {form_data.username}")   

        user = await self.repository.get_by_username(
            form_data.username
        )

        if (
            user is None
            or not verify_password(
                form_data.password,
                user.password,
            )
        ):
            logger.warning(f"Invalid credentials for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = create_access_token(
            data={
                "sub": user.username
            }
        )

        return Token(
            access_token=access_token
        )