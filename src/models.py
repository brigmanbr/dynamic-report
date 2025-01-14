from typing import List, Optional
from pydantic import BaseModel, Field

class CamelModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

class Message(BaseModel):
    id: int
    text: str
    timestamp: str
    report_id: Optional[int] = None

class Report(BaseModel):
    id: int
    name: str
    credit_cost: int

class UsageData(BaseModel):
    id: int
    timestamp: str
    credits: float
    report_name: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        if d.get('report_name') is None:
            d.pop('report_name', None)
        return d

class UsageResponse(BaseModel):
    usage: List[UsageData]

    class Config:
        json_encoders = {
            UsageData: lambda v: {k: v for k, v in v.dict().items() if v is not None}
        }
