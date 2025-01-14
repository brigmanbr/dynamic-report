from fastapi import APIRouter, HTTPException
from services.usage_service import UsageService
from models import UsageResponse
from config import BASE_MESSAGES_URL, BASE_REPORTS_URL

router = APIRouter()

usage_service = UsageService(BASE_MESSAGES_URL, BASE_REPORTS_URL)

@router.get("/usage", response_model=UsageResponse)
async def get_usage():
    try:
        usage_data = await usage_service.get_usage_data()
        return usage_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
