from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_ref = Column(String, unique=True, nullable=False)      # e.g. "RPT-20240501"
    generated_at = Column(DateTime, default=datetime.utcnow)
    trade_count = Column(Integer, nullable=False)
    failed_count = Column(Integer, nullable=False)
    file_path = Column(String, nullable=True)                     # path to CSV/XML file
    regulation = Column(String, default="EMIR")                  # EMIR or MiFID2