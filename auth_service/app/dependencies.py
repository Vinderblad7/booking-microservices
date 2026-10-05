from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import decode_token
from app.exceptions import (
    InsufficientPermissionsError,
    InvalidTokenError,
    UserInactiveError,
    UserNotFoundError,
)
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_repo(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]


async def get_user_service(user_repo: UserRepoDep) -> UserService:
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: UserRepoDep,
) -> User:
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise InvalidTokenError("Invalid or expired access token")

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenError("Token subject is missing")

    user = await user_repo.get_by_id(int(user_id_str))
    if not user:
        raise UserNotFoundError(f"User with id {user_id_str} not found")

    if not user.is_active:
        raise UserInactiveError("User account is inactive")

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_admin(current_user: CurrentUserDep) -> User:
    if current_user.role != UserRole.ADMIN:
        raise InsufficientPermissionsError("Admin privileges required")
    return current_user


CurrentAdminDep = Annotated[User, Depends(get_current_admin)]