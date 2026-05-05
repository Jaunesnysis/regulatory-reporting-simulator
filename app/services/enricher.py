from app.models.trade import Trade, InstrumentType


INSTRUMENT_ASSET_CLASS = {
    InstrumentType.FX_SPOT: "Foreign Exchange",
    InstrumentType.FX_FORWARD: "Foreign Exchange",
    InstrumentType.INTEREST_RATE_SWAP: "Rates",
    InstrumentType.BOND: "Credit",
    InstrumentType.EQUITY: "Equity",
}

REPORTING_DEADLINES_DAYS = {
    InstrumentType.FX_SPOT: 1,
    InstrumentType.FX_FORWARD: 1,
    InstrumentType.INTEREST_RATE_SWAP: 1,
    InstrumentType.BOND: 1,
    InstrumentType.EQUITY: 1,
}


def enrich_trade(trade: Trade) -> dict:
    """
    Enriches a validated trade with additional regulatory metadata.
    Returns a dict of enriched fields (not stored in DB, used in report).
    """
    from datetime import timedelta

    deadline_days = REPORTING_DEADLINES_DAYS.get(trade.instrument_type, 1)
    reporting_deadline = trade.trade_date + timedelta(days=deadline_days)

    return {
        "asset_class": INSTRUMENT_ASSET_CLASS.get(trade.instrument_type, "Unknown"),
        "reporting_deadline": reporting_deadline.strftime("%Y-%m-%d"),
        "regulation": "EMIR",
        "report_status": "PENDING_SUBMISSION",
    }