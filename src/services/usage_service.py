from repositories.message_repository import MessageRepository
from repositories.report_repository import ReportRepository
from utils.credit_calculator import calculate_credits
from models import UsageResponse, UsageData, Message

class UsageService:
    def __init__(self, messages_url: str, reports_url: str):
        self.message_repo = MessageRepository(messages_url)
        self.report_repo = ReportRepository(reports_url)

    async def get_usage_data(self) -> UsageResponse:
        messages = await self.message_repo.fetch_messages()
        usage_data = []

        for message_dict in messages:
            message = Message(**message_dict)
            report = None
            credits = 0.0

            if message.report_id:
                report = await self.report_repo.fetch_report(message.report_id)

            if report:
                credits = report.credit_cost
                report_name = report.name
            else:
                credits = calculate_credits(message.text)
                report_name = None

            usage_data.append(
                UsageData(
                    id=message.id,
                    timestamp=message.timestamp,
                    credits=credits,
                    report_name=report_name,
                )
            )
        return UsageResponse(usage=usage_data)
