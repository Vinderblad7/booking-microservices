from httpx import AsyncClient


async def test_get_bookings_empty_or_list(client: AsyncClient) -> None:
    response = await client.get("/api/bookings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_booking_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Booking Hotel", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "101", "price": 100, "capacity": 2}
    )
    room_id = room_res.json()["id"]

    payload = {
        "room_id": room_id,
        "check_in": "2026-10-01",
        "check_out": "2026-10-10"
    }

    response = await client.post("/api/bookings", json=payload, params={"user_id": 1})

    assert response.status_code == 201
    data = response.json()
    assert data["room_id"] == room_id
    assert data["check_in"] == "2026-10-01"
    assert data["check_out"] == "2026-10-10"
    assert "id" in data

    booking_id = data["id"]
    get_res = await client.get(f"/api/bookings/{booking_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == booking_id


async def test_create_booking_invalid_data(client: AsyncClient):
    invalid_payload = {
        "check_in": "2026-10-01"
    }

    response = await client.post("/api/bookings", json=invalid_payload, params={"user_id": 1})

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


async def test_check_room_availability_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Availability Hotel", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "102", "price": 120, "capacity": 2}
    )
    room_id = room_res.json()["id"]

    params = {
        "room_id": room_id,
        "check_in": "2026-11-01",
        "check_out": "2026-11-05"
    }

    response = await client.get("/api/bookings/check-availability", params=params)

    assert response.status_code == 200
    assert isinstance(response.json(), bool)


async def test_get_booking_by_id_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Hotel Get Booking", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "103", "price": 150, "capacity": 2}
    )
    room_id = room_res.json()["id"]

    booking_res = await client.post(
        "/api/bookings",
        json={"room_id": room_id, "check_in": "2026-12-01", "check_out": "2026-12-05"},
        params={"user_id": 1}
    )
    booking_id = booking_res.json()["id"]

    response = await client.get(f"/api/bookings/{booking_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == booking_id
    assert data["room_id"] == room_id


async def test_get_booking_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/bookings/99999")
    assert response.status_code == 404


async def test_update_booking_status_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Hotel Update Status", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "104", "price": 180, "capacity": 2}
    )
    room_id = room_res.json()["id"]

    booking_res = await client.post(
        "/api/bookings",
        json={"room_id": room_id, "check_in": "2026-12-10", "check_out": "2026-12-15"},
        params={"user_id": 1}
    )
    booking_id = booking_res.json()["id"]

    new_status = {"status": "cancelled"}

    update_response = await client.patch(
        f"/api/bookings/{booking_id}/status",
        json=new_status
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "cancelled"


async def test_delete_booking_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Hotel Delete Booking", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "105", "price": 200, "capacity": 2}
    )
    room_id = room_res.json()["id"]

    booking_res = await client.post(
        "/api/bookings",
        json={"room_id": room_id, "check_in": "2026-12-20", "check_out": "2026-12-25"},
        params={"user_id": 1}
    )
    booking_id = booking_res.json()["id"]

    delete_response = await client.delete(f"/api/bookings/{booking_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/bookings/{booking_id}")
    assert get_response.status_code == 404


async def test_delete_booking_not_found(client: AsyncClient):
    delete_response = await client.delete("/api/bookings/99999")
    assert delete_response.status_code == 404