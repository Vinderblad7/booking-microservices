import jwt

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserInactiveError,
    UserNotFoundError,
)
from app.repositories.user import UserRepository
from app.schemas.user import TokenResponse, UserLogin, UserRegister, UserResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return UserResponse.model_validate(user)

    async def get_by_email(self, email: str) -> UserResponse:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UserNotFoundError(f"User with email {email} not found")
        return UserResponse.model_validate(user)

    async def register(self, user_data: UserRegister) -> UserResponse:
        user_exist = await self.user_repo.get_by_email(user_data.email)
        if user_exist:
            raise UserAlreadyExistsError(f"User with email {user_data.email} already exists")

        data = user_data.model_dump(exclude={"password"})
        data["hashed_password"] = hash_password(user_data.password)

        user = await self.user_repo.create(data)
        return UserResponse.model_validate(user)

    async def login(self, creds: UserLogin) -> TokenResponse:
        user = await self.user_repo.get_by_email(creds.email)
        if not user or not verify_password(creds.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise UserInactiveError("User account is inactive")

        role_value = user.role.value if hasattr(user.role, "value") else str(user.role)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": role_value,
            }
        )
        refresh_token = create_refresh_token(user_id=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError:
            raise InvalidTokenError("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token type")

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise InvalidTokenError("Token subject is missing")

        user = await self.user_repo.get_by_id(int(user_id_str))
        if not user:
            raise UserNotFoundError(f"User with id {user_id_str} not found")

        if not user.is_active:
            raise UserInactiveError("User account is inactive")

        role_value = user.role.value if hasattr(user.role, "value") else str(user.role)
        new_access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": role_value,
            }
        )
        new_refresh_token = create_refresh_token(user_id=user.id)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
