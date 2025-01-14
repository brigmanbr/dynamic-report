import httpx
from typing import Optional
from models import Report

async def fetch_report(base_url: str, report_id: int) -> Optional[Report]:
    url = f"{base_url}/{report_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return Report(**response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except httpx.RequestError:
            print(f"Network error occurred while fetching report {report_id}")
            return None
