from httpx import AsyncClient


async def test_health_or_empty_hotels(client: AsyncClient) -> None:
    response = await client.get("/api/hotels")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_hotel_success(client: AsyncClient):
    payload = {
        "name": "test hotel",
        "description": "test description"
    }

    response = await client.post("/api/hotels", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test hotel"
    assert data["description"] == "test description"
    assert "id" in data

    hotel_id = data["id"]
    get_response = await client.get(f"/api/hotels/{hotel_id}")
    
    assert get_response.status_code == 200
    assert get_response.json()["id"] == hotel_id


async def test_create_hotel_invalid_data(client: AsyncClient):
    invalid_payload = {
        "description": "test description"
    }

    response = await client.post("/api/hotels", json=invalid_payload)

    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


async def test_get_hotels(client: AsyncClient):
    response = await client.get("/api/hotels")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_hotel_by_id_success(client: AsyncClient):
    create_response = await client.post(
        "/api/hotels", 
        json={"name": "Test Hotel", "description": "Test Desc"}
    )
    created_hotel = create_response.json()
    hotel_id = created_hotel["id"]

    response = await client.get(f"/api/hotels/{hotel_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == hotel_id
    assert data["name"] == "Test Hotel"


async def test_get_hotel_by_id_not_found(client: AsyncClient):
    response = await client.get("/api/hotels/99999")
    assert response.status_code == 404


async def test_get_hotel_by_slug_success(client: AsyncClient):
    create_response = await client.post(
        "/api/hotels", 
        json={"name": "Test Hotel Slug", "description": "Test Desc"}
    )
    created_hotel = create_response.json()
    hotel_slug = created_hotel["slug"]

    response = await client.get(f"/api/hotels/by-slug/{hotel_slug}")

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == hotel_slug
    assert data["name"] == "Test Hotel Slug"


async def test_get_hotel_by_slug_not_found(client: AsyncClient):
    response = await client.get("/api/hotels/by-slug/non-existent-hotel-slug")
    assert response.status_code == 404


async def test_update_hotel_success(client: AsyncClient):
    create_response = await client.post(
        "/api/hotels", 
        json={"name": "Test Hotel", "description": "Test Desc"}
    )
    created_hotel = create_response.json()
    hotel_id = created_hotel["id"]

    new_data = {"name": "Updated Hotel", "description": "Test Desc"}

    update_response = await client.patch(
        f"/api/hotels/{hotel_id}",
        json=new_data
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated Hotel"
    assert data["description"] == "Test Desc"


async def test_delete_hotel_success(client: AsyncClient):
    create_response = await client.post(
        "/api/hotels", 
        json={"name": "Test Hotel", "description": "Test Desc"}
    )
    created_hotel = create_response.json()
    hotel_id = created_hotel["id"]

    delete_response = await client.delete(f"/api/hotels/{hotel_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/hotels/{hotel_id}")
    assert get_response.status_code == 404


async def test_delete_hotel_not_found(client: AsyncClient):
    delete_response = await client.delete("/api/hotels/99999")
    assert delete_response.status_code == 404