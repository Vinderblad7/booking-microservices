from httpx import AsyncClient


async def test_register_success(client: AsyncClient) -> None:
    payload = {
        "email": "user@example.com",
        "password": "strongpassword123",
    }
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data


async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {
        "email": "duplicate@example.com",
        "password": "strongpassword123",
    }
    res1 = await client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/auth/register", json=payload)
    assert res2.status_code == 409
    assert "already exists" in res2.json()["detail"]


async def test_register_invalid_data(client: AsyncClient) -> None:
    payload = {
        "email": "test@example.com",
        "password": "123",
    }
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 422


async def test_login_success(client: AsyncClient) -> None:
    reg_payload = {"email": "login@example.com", "password": "mypassword123"}
    await client.post("/api/auth/register", json=reg_payload)

    login_payload = {"email": "login@example.com", "password": "mypassword123"}
    response = await client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient) -> None:
    reg_payload = {"email": "wrongpass@example.com", "password": "correctpassword"}
    await client.post("/api/auth/register", json=reg_payload)

    login_payload = {"email": "wrongpass@example.com", "password": "incorrectpassword"}
    response = await client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


async def test_login_nonexistent_user(client: AsyncClient) -> None:
    login_payload = {"email": "nosuchuser@example.com", "password": "somepassword"}
    response = await client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401


async def test_refresh_tokens_success(client: AsyncClient) -> None:
    reg_payload = {"email": "refresh@example.com", "password": "mypassword123"}
    await client.post("/api/auth/register", json=reg_payload)

    login_res = await client.post("/api/auth/login", json=reg_payload)
    refresh_token = login_res.json()["refresh_token"]

    refresh_res = await client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_res.status_code == 200
    data = refresh_res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_refresh_tokens_with_invalid_token(client: AsyncClient) -> None:
    response = await client.post("/api/auth/refresh", json={"refresh_token": "invalid.jwt.token"})
    assert response.status_code == 401


async def test_get_me_authorized(client: AsyncClient) -> None:
    reg_payload = {"email": "me@example.com", "password": "mypassword123"}
    await client.post("/api/auth/register", json=reg_payload)

    login_res = await client.post("/api/auth/login", json=reg_payload)
    access_token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    me_res = await client.get("/api/auth/me", headers=headers)
    assert me_res.status_code == 200
    data = me_res.json()
    assert data["email"] == "me@example.com"
    assert data["role"] == "user"


async def test_get_me_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/api/auth/me")
    assert response.status_code == 401
