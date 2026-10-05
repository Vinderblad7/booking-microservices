from fastapi import APIRouter, status

from app.dependencies import CurrentUserDep, UserServiceDep
from app.schemas.user import (
    TokenRefreshRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    user_service: UserServiceDep,
):
    return await user_service.register(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    creds: UserLogin,
    user_service: UserServiceDep,
):
    return await user_service.login(creds)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    data: TokenRefreshRequest,
    user_service: UserServiceDep,
):
    return await user_service.refresh_tokens(data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUserDep):
    return current_user
