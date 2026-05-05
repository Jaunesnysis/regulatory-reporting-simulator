from sqlalchemy import Column, String, Float, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum
from datetime import datetime


class InstrumentType(str, enum.Enum):
    FX_SPOT = "FX_SPOT"
    FX_FORWARD = "FX_FORWARD"
    INTEREST_RATE_SWAP = "INTEREST_RATE_SWAP"
    BOND = "BOND"
    EQUITY = "EQUITY"


class TradeStatus(str, enum.Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    REPORTED = "REPORTED"


class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_ref = Column(String, unique=True, nullable=False)       # e.g. "TRD-20240501-001"
    counterparty_lei = Column(String(20), nullable=False)         # Legal Entity Identifier
    instrument_type = Column(SAEnum(InstrumentType), nullable=False)
    notional = Column(Float, nullable=False)                      # trade value
    currency = Column(String(3), nullable=False)                  # ISO 4217 e.g. "EUR"
    trade_date = Column(DateTime, nullable=False)
    settlement_date = Column(DateTime, nullable=False)
    venue = Column(String, nullable=True)                         # where trade was executed
    status = Column(SAEnum(TradeStatus), default=TradeStatus.PENDING)
    validation_error = Column(String, nullable=True)              # reason if failed
    created_at = Column(DateTime, default=datetime.utcnow)