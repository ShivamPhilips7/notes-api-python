from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.auth import UserRegister
from app.security.password import hash_password
from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_register_user(mock_user_repository):
    """
    Test successful user registration.
    """

    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.get_by_email.return_value = None

    user = User(
        username="ash",
        email="ash@example.com",
        password=hash_password("password123"),
        created_at=datetime.now(),
    )

    mock_user_repository.create_user.return_value = user

    service = AuthService(mock_user_repository)

    request = UserRegister(
        username="ash",
        email="ash@example.com",
        password="password123",
    )

    result = await service.register(request)

    assert result.username == "ash"
    assert result.email == "ash@example.com"

    mock_user_repository.get_by_username.assert_called_once_with("ash")
    mock_user_repository.get_by_email.assert_called_once_with(
        "ash@example.com"
    )
    mock_user_repository.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_duplicate_username(mock_user_repository):
    """
    Test registration with an existing username.
    """

    mock_user_repository.get_by_username.return_value = object()

    service = AuthService(mock_user_repository)

    request = UserRegister(
        username="ash",
        email="ash@example.com",
        password="password123",
    )

    with pytest.raises(HTTPException) as exc:
        await service.register(request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Username already exists"

    mock_user_repository.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_register_duplicate_email(mock_user_repository):
    """
    Test registration with an existing email.
    """

    mock_user_repository.get_by_username.return_value = None
    mock_user_repository.get_by_email.return_value = object()

    service = AuthService(mock_user_repository)

    request = UserRegister(
        username="ash",
        email="ash@example.com",
        password="password123",
    )

    with pytest.raises(HTTPException) as exc:
        await service.register(request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already exists"

    mock_user_repository.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_login_success(mock_user_repository):
    """
    Test successful login.
    """

    user = User(
        username="ash",
        email="ash@example.com",
        password=hash_password("password123"),
        created_at=datetime.now(),
    )

    mock_user_repository.get_by_username.return_value = user

    service = AuthService(mock_user_repository)

    form = OAuth2PasswordRequestForm(
        username="ash",
        password="password123",
        scope="",
        client_id=None,
        client_secret=None,
    )

    token = await service.authenticate(form)

    assert token.access_token is not None
    assert token.token_type == "bearer"

    mock_user_repository.get_by_username.assert_called_once_with("ash")


@pytest.mark.asyncio
async def test_login_invalid_password(mock_user_repository):
    """
    Test login with an invalid password.
    """

    user = User(
        username="ash",
        email="ash@example.com",
        password=hash_password("password123"),
        created_at=datetime.now(),
    )

    mock_user_repository.get_by_username.return_value = user

    service = AuthService(mock_user_repository)

    form = OAuth2PasswordRequestForm(
        username="ash",
        password="wrongpassword",
        scope="",
        client_id=None,
        client_secret=None,
    )

    with pytest.raises(HTTPException) as exc:
        await service.authenticate(form)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_user_not_found(mock_user_repository):
    """
    Test login with a non-existent username.
    """

    mock_user_repository.get_by_username.return_value = None

    service = AuthService(mock_user_repository)

    form = OAuth2PasswordRequestForm(
        username="unknown",
        password="password123",
        scope="",
        client_id=None,
        client_secret=None,
    )

    with pytest.raises(HTTPException) as exc:
        await service.authenticate(form)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid username or password"