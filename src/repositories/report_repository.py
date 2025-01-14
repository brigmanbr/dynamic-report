import httpx
from models import Report
from typing import Optional

class ReportRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_report(self, report_id: int) -> Optional[Report]:
        url = f"{self.base_url}/{report_id}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return Report(**response.json())
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise e
            except httpx.RequestError:
                return None
