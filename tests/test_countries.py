import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_countries_success(async_client):
    response = await async_client.get("/countries")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "name" in data[0]
    assert "official_name" in data[0]
    assert "flag_url" in data[0]
    assert "is_long_name" in data[0]

@pytest.mark.asyncio
async def test_get_countries_with_search_filter(async_client):
    response = await async_client.get("/countries?search=Brazil")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    brazil_found = any("brazil" in str(country["name"]).lower() for country in data)
    assert brazil_found
