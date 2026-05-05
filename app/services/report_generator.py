import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.trade import Trade, TradeStatus
from app.models.report import Report
from app.services.enricher import enrich_trade
import uuid


REPORTS_DIR = "reports_output"


def generate_csv_report(db: Session) -> Report:
    """
    Fetches all validated trades, enriches them,
    writes a CSV report, and saves a Report record to DB.
    """

    validated_trades = db.query(Trade).filter(
        Trade.status == TradeStatus.VALIDATED
    ).all()

    failed_trades = db.query(Trade).filter(
        Trade.status == TradeStatus.FAILED
    ).all()

    os.makedirs(REPORTS_DIR, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_ref = f"RPT-{timestamp}"
    file_name = f"{report_ref}.csv"
    file_path = os.path.join(REPORTS_DIR, file_name)

    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Header row
        writer.writerow([
            "trade_ref",
            "counterparty_lei",
            "instrument_type",
            "asset_class",
            "notional",
            "currency",
            "trade_date",
            "settlement_date",
            "venue",
            "reporting_deadline",
            "regulation",
            "report_status",
        ])

        for trade in validated_trades:
            enriched = enrich_trade(trade)
            writer.writerow([
                trade.trade_ref,
                trade.counterparty_lei,
                trade.instrument_type.value,
                enriched["asset_class"],
                trade.notional,
                trade.currency,
                trade.trade_date.strftime("%Y-%m-%d"),
                trade.settlement_date.strftime("%Y-%m-%d"),
                trade.venue or "XOFF",
                enriched["reporting_deadline"],
                enriched["regulation"],
                enriched["report_status"],
            ])

    report = Report(
        id=uuid.uuid4(),
        report_ref=report_ref,
        trade_count=len(validated_trades),
        failed_count=len(failed_trades),
        file_path=file_path,
        regulation="EMIR",
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report