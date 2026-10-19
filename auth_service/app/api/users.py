from fastapi import APIRouter, Query, status

from app.dependencies import CurrentAdminDep, UserServiceDep
from app.models.user import UserRole
from app.schemas.user import (
    UserAdminCreate,
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserResponse])
async def get_users(
    user_service: UserServiceDep,
    _: CurrentAdminDep,
    role: UserRole | None = None,
    is_active: bool | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await user_service.get_all(
        role=role,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserServiceDep,
    _: CurrentAdminDep,
):
    return await user_service.get_by_id(user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_by_admin(
    user_data: UserAdminCreate,
    user_service: UserServiceDep,
    _: CurrentAdminDep,
):
    return await user_service.create_by_admin(user_data)


@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    data: UserRoleUpdate,
    user_service: UserServiceDep,
    _: CurrentAdminDep,
):
    return await user_service.update_role(user_id, data.role)


@router.patch("/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: int,
    data: UserStatusUpdate,
    user_service: UserServiceDep,
    _: CurrentAdminDep,
):
    return await user_service.update_status(user_id, data.is_active)
