from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.dependencies import SessionDep
from app.exceptions import InvalidTokenError
from app.repositories.payment import PaymentRepository
from app.services.payment import PaymentService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_payment_service(session: SessionDep) -> PaymentService:
    payment_repo = PaymentRepository(session)
    return PaymentService(payment_repo=payment_repo)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise InvalidTokenError("Invalid or expired access token")

    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenError("Token subject is missing")

    return int(user_id_str)


PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]
CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]
