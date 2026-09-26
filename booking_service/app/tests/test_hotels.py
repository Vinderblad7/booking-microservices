from httpx import AsyncClient


async def test_health_or_empty_hotels(client: AsyncClient) -> None:
    response = await client.get("/api/hotels")
    assert response.status_code == 200
    assert response.json() == []