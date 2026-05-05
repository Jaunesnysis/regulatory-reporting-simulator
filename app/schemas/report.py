from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class ReportResponse(BaseModel):
    id: UUID
    report_ref: str
    generated_at: datetime
    trade_count: int
    failed_count: int
    file_path: Optional[str]
    regulation: str

    class Config:
        from_attributes = True