from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.trade import InstrumentType, TradeStatus


class TradeCreate(BaseModel):
    trade_ref: str = Field(..., example="TRD-20240501-001")
    counterparty_lei: str = Field(..., min_length=20, max_length=20, example="SWEDBANK00LEI0000001")
    instrument_type: InstrumentType
    notional: float = Field(..., gt=0, example=1000000.0)
    currency: str = Field(..., min_length=3, max_length=3, example="EUR")
    trade_date: datetime
    settlement_date: datetime
    venue: Optional[str] = None


class TradeResponse(BaseModel):
    id: UUID
    trade_ref: str
    counterparty_lei: str
    instrument_type: InstrumentType
    notional: float
    currency: str
    trade_date: datetime
    settlement_date: datetime
    venue: Optional[str]
    status: TradeStatus
    validation_error: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True