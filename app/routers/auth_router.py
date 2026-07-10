import logging
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_auth_service
from app.models.user import User
from app.schemas.auth import Token, UserRegister, UserResponse
from app.services.auth_service import AuthService
from app.security.roles import require_role

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    request: UserRegister,
    service: AuthService = Depends(get_auth_service),
):
    logger.info(f"Registering user: {request.username}")
    return await service.register(request)


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    logger.info(f"Authenticating user: {form_data.username}")
    return await service.authenticate(form_data)

@router.get(
    "/users",
    response_model=list[UserResponse],
)
async def get_all_users(
    service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(require_role("ADMIN")),
):
    return await service.get_all_users()