import pytest
import httpx
from services import fetch_report

@pytest.mark.asyncio
async def test_fetch_report_success(monkeypatch):
    base_url = "http://test.com/reports"
    mock_report = {"id": 1, "name": "Test Report", "credit_cost": 10}

    async def mock_get(self, url, **kwargs):
        request = httpx.Request("GET", url)
        return httpx.Response(200, json=mock_report, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    result = await fetch_report(base_url, 1)
    assert result.id == 1
    assert result.name == "Test Report"
    assert result.credit_cost == 10

@pytest.mark.asyncio
async def test_fetch_report_not_found(monkeypatch):
    base_url = "http://test.com/reports"

    async def mock_get(self, url, **kwargs):
        request = httpx.Request("GET", url)
        return httpx.Response(404, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    result = await fetch_report(base_url, 999)
    assert result is None
