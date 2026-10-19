from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password
from app.models.user import User, UserRole


async def create_test_user(session: AsyncSession, email: str, role: UserRole) -> User:
    user = User(
        email=email,
        hashed_password=hash_password("password123"),
        role=role,
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def test_get_users_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/api/users")
    assert response.status_code == 401


async def test_get_users_forbidden_for_normal_user(client: AsyncClient, db_session: AsyncSession) -> None:
    user = await create_test_user(db_session, "user@test.com", UserRole.USER)
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role.value})
    response = await client.get("/api/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


async def test_get_users_as_admin(client: AsyncClient, db_session: AsyncSession) -> None:
    admin = await create_test_user(db_session, "admin@test.com", UserRole.ADMIN)
    token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": admin.role.value})
    response = await client.get("/api/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


async def test_admin_create_user(client: AsyncClient, db_session: AsyncSession) -> None:
    admin = await create_test_user(db_session, "admin_creator@test.com", UserRole.ADMIN)
    token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": admin.role.value})

    payload = {
        "email": "new_admin@test.com",
        "password": "strongpassword",
        "role": "admin",
        "is_active": True,
    }
    response = await client.post("/api/users", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new_admin@test.com"
    assert data["role"] == "admin"


async def test_admin_update_role(client: AsyncClient, db_session: AsyncSession) -> None:
    admin = await create_test_user(db_session, "admin_updater@test.com", UserRole.ADMIN)
    target_user = await create_test_user(db_session, "target@test.com", UserRole.USER)
    token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": admin.role.value})

    patch_res = await client.patch(
        f"/api/users/{target_user.id}/role",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["role"] == "admin"


async def test_admin_update_status(client: AsyncClient, db_session: AsyncSession) -> None:
    admin = await create_test_user(db_session, "admin_status@test.com", UserRole.ADMIN)
    target_user = await create_test_user(db_session, "target_status@test.com", UserRole.USER)
    token = create_access_token({"sub": str(admin.id), "email": admin.email, "role": admin.role.value})

    patch_res = await client.patch(
        f"/api/users/{target_user.id}/status",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["is_active"] is False
