import pytest
import httpx
from repositories.report_repository import ReportRepository  # Importing the correct class
from models import Report  # Ensure you import the Report model

@pytest.mark.asyncio
async def test_fetch_report_success(monkeypatch):
    base_url = "http://test.com/reports"
    mock_report_data = {"id": 1, "name": "Test Report", "credit_cost": 10}

    # Create a mock response object
    class MockResponse:
        def __init__(self, json_data):
            self._json_data = json_data
            self.status_code = 200  # Set a status code for success

        def json(self):
            return self._json_data  # Return the mock JSON data synchronously

        def raise_for_status(self):
            # This method does nothing for successful responses
            pass

    # Mocking the async get method of httpx.AsyncClient
    async def mock_get(url, *args, **kwargs):
        return MockResponse(mock_report_data)

    # Replace the get method on httpx.AsyncClient with our mock_get
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    report_repo = ReportRepository(base_url)  # Create an instance of ReportRepository
    result = await report_repo.fetch_report(1)  # Call fetch_report on the instance

    assert result.id == 1
    assert result.name == "Test Report"
    assert result.credit_cost == 10

@pytest.mark.asyncio
async def test_fetch_report_not_found(monkeypatch):
    base_url = "http://test.com/reports"

    # Create a mock response object for 404
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

        def json(self):
            return None  # Return None synchronously

        def raise_for_status(self):
            raise httpx.HTTPStatusError("Not Found", request=None, response=self)

    # Mocking the async get method of httpx.AsyncClient for a 404 response
    async def mock_get(url, *args, **kwargs):
        return MockResponse(404)

    # Replace the get method on httpx.AsyncClient with our mock_get
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    report_repo = ReportRepository(base_url)  # Create an instance of ReportRepository
    result = await report_repo.fetch_report(999)  # Call fetch_report on the instance

    assert result is None
