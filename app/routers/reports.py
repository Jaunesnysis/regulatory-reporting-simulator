from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.report import Report
from app.schemas.report import ReportResponse
from app.services.report_generator import generate_csv_report
from typing import List

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(db: Session = Depends(get_db)):
    """Generate a CSV regulatory report from all validated trades."""
    report = generate_csv_report(db)
    return report


@router.get("/", response_model=List[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    """Get all generated reports."""
    return db.query(Report).all()