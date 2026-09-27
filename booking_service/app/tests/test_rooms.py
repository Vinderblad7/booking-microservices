from httpx import AsyncClient


async def test_get_rooms_empty_or_list(client: AsyncClient) -> None:
    response = await client.get("/api/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_room_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Grand Hotel", "description": "Luxury hotel"}
    )
    assert hotel_res.status_code == 201
    hotel_id = hotel_res.json()["id"]

    payload = {
        "hotel_id": hotel_id,
        "number": "101",
        "price": 100,
        "capacity": 2
    }

    response = await client.post("/api/rooms", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["hotel_id"] == hotel_id
    assert data["number"] == "101"
    assert float(data["price"]) == 100
    assert data["capacity"] == 2
    assert "id" in data

    room_id = data["id"]
    get_res = await client.get(f"/api/rooms/{room_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == room_id


async def test_create_room_invalid_data(client: AsyncClient):
    invalid_payload = {
        "number": "102"
    }

    response = await client.post("/api/rooms", json=invalid_payload)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


async def test_create_room_non_existent_hotel(client: AsyncClient):
    payload = {
        "hotel_id": 99999,
        "number": "999",
        "price": 100,
        "capacity": 2
    }

    response = await client.post("/api/rooms", json=payload)
    assert response.status_code in [404, 400]


async def test_get_rooms(client: AsyncClient):
    response = await client.get("/api/rooms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_room_by_id_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Test Hotel Room", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "201", "price": 150, "capacity": 2}
    )
    created_room = room_res.json()
    room_id = created_room["id"]

    response = await client.get(f"/api/rooms/{room_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == room_id
    assert data["number"] == "201"


async def test_get_room_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/rooms/99999")
    assert response.status_code == 404


async def test_update_room_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Hotel for Update", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "301", "price": 200, "capacity": 3}
    )
    room_id = room_res.json()["id"]

    new_data = {"number": "301-A", "price": 250}

    update_response = await client.patch(
        f"/api/rooms/{room_id}",
        json=new_data
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["number"] == "301-A"
    assert float(data["price"]) == 250


async def test_delete_room_success(client: AsyncClient):
    hotel_res = await client.post(
        "/api/hotels",
        json={"name": "Hotel for Delete", "description": "Desc"}
    )
    hotel_id = hotel_res.json()["id"]

    room_res = await client.post(
        "/api/rooms",
        json={"hotel_id": hotel_id, "number": "401", "price": 300, "capacity": 4}
    )
    room_id = room_res.json()["id"]

    delete_response = await client.delete(f"/api/rooms/{room_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/rooms/{room_id}")
    assert get_response.status_code == 404


async def test_delete_room_not_found(client: AsyncClient):
    delete_response = await client.delete("/api/rooms/99999")
    assert delete_response.status_code == 404