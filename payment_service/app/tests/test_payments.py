from httpx import AsyncClient


async def test_get_payments_empty_list(client: AsyncClient):
    response = await client.get("/api/payments")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_payment_success(client: AsyncClient, auth_headers: dict[str, str]):
    payload = {"booking_id": 1, "amount": "150.00"}
    response = await client.post("/api/payments", json=payload, headers=auth_headers)
    assert response.status_code == 201

    data = response.json()
    assert data["booking_id"] == 1
    assert data["user_id"] == 1
    assert data["amount"] == "150.00"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_create_payment_unauthorized(client: AsyncClient):
    payload = {"booking_id": 1, "amount": "150.00"}
    response = await client.post("/api/payments", json=payload)
    assert response.status_code == 401


async def test_create_payment_invalid_amount(
    client: AsyncClient, auth_headers: dict[str, str]
):
    payload = {"booking_id": 1, "amount": "-10.00"}
    response = await client.post("/api/payments", json=payload, headers=auth_headers)
    assert response.status_code == 422


async def test_get_payment_by_id(client: AsyncClient, auth_headers: dict[str, str]):
    create_res = await client.post(
        "/api/payments",
        json={"booking_id": 1, "amount": "200.00"},
        headers=auth_headers,
    )
    payment_id = create_res.json()["id"]

    response = await client.get(f"/api/payments/{payment_id}")
    assert response.status_code == 200
    assert response.json()["id"] == payment_id
    assert response.json()["booking_id"] == 1


async def test_get_payment_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/payments/9999")
    assert response.status_code == 404


async def test_get_payment_by_booking_id(
    client: AsyncClient, auth_headers: dict[str, str]
):
    await client.post(
        "/api/payments",
        json={"booking_id": 10, "amount": "300.00"},
        headers=auth_headers,
    )

    response = await client.get("/api/payments/booking/10")
    assert response.status_code == 200
    assert response.json()["booking_id"] == 10
    assert response.json()["amount"] == "300.00"


async def test_get_payment_by_booking_id_not_found(client: AsyncClient):
    response = await client.get("/api/payments/booking/9999")
    assert response.status_code == 404


async def test_get_my_payments(client: AsyncClient, auth_headers: dict[str, str]):
    await client.post(
        "/api/payments",
        json={"booking_id": 21, "amount": "100.00"},
        headers=auth_headers,
    )

    response = await client.get("/api/payments/my", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["user_id"] == 1


async def test_process_payment_success(
    client: AsyncClient, auth_headers: dict[str, str]
):
    create_res = await client.post(
        "/api/payments",
        json={"booking_id": 30, "amount": "500.00"},
        headers=auth_headers,
    )
    payment_id = create_res.json()["id"]

    pay_res = await client.post(
        f"/api/payments/{payment_id}/pay",
        json={"card_number": "4242424242424242"},
        headers=auth_headers,
    )
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "success"


async def test_process_payment_failed(client: AsyncClient, auth_headers: dict[str, str]):
    create_res = await client.post(
        "/api/payments",
        json={"booking_id": 31, "amount": "500.00"},
        headers=auth_headers,
    )
    payment_id = create_res.json()["id"]

    pay_res = await client.post(
        f"/api/payments/{payment_id}/pay",
        json={"card_number": "11110000"},
        headers=auth_headers,
    )
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "failed"


async def test_process_payment_already_processed(
    client: AsyncClient, auth_headers: dict[str, str]
):
    create_res = await client.post(
        "/api/payments",
        json={"booking_id": 32, "amount": "500.00"},
        headers=auth_headers,
    )
    payment_id = create_res.json()["id"]

    await client.post(
        f"/api/payments/{payment_id}/pay",
        json={"card_number": "4242424242424242"},
        headers=auth_headers,
    )

    second_pay = await client.post(
        f"/api/payments/{payment_id}/pay",
        json={"card_number": "4242424242424242"},
        headers=auth_headers,
    )
    assert second_pay.status_code == 409


async def test_create_duplicate_payment_when_already_success(
    client: AsyncClient, auth_headers: dict[str, str]
):
    create_res = await client.post(
        "/api/payments",
        json={"booking_id": 33, "amount": "250.00"},
        headers=auth_headers,
    )
    payment_id = create_res.json()["id"]

    await client.post(
        f"/api/payments/{payment_id}/pay",
        json={"card_number": "4242424242424242"},
        headers=auth_headers,
    )

    duplicate_res = await client.post(
        "/api/payments",
        json={"booking_id": 33, "amount": "250.00"},
        headers=auth_headers,
    )
    assert duplicate_res.status_code == 409
