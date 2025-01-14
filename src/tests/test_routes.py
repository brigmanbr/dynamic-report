import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_get_usage_success():
    async with AsyncClient(app=app, base_url="http://usage") as ac:
        response = await ac.get("/usage")
        assert response.status_code == 200
        assert "usage" in response.json()

@pytest.mark.asyncio
async def test_get_usage_bad_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/usages")
        assert response.status_code == 404
