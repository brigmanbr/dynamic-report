from fastapi import APIRouter, HTTPException
from models import UsageResponse, Message, UsageData
from services import fetch_report
from utils import calculate_credits
from config import BASE_MESSAGES_URL, BASE_REPORTS_URL
import httpx

usage_router = APIRouter()

@usage_router.get("/usage", response_model=UsageResponse)
async def get_usage():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_MESSAGES_URL)
            response.raise_for_status()
            messages = response.json().get("messages", [])

            usage_data = []
            for message_dict in messages:
                message = Message(**message_dict)
                report = await fetch_report(BASE_REPORTS_URL, message.report_id) if message.report_id else None

                if report:
                    credits = report.credit_cost
                    report_name = report.name
                else:
                    credits = calculate_credits(message.text)
                    report_name = None

                usage_entry = UsageData(
                    id=message.id,
                    timestamp=message.timestamp,
                    credits=credits,
                    report_name=report_name
                )
                usage_data.append(usage_entry)

            return UsageResponse(usage=usage_data)

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
