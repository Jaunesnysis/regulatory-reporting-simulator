from app.models.trade import Trade, TradeStatus
from datetime import datetime, timezone


VALID_CURRENCIES = {"EUR", "USD", "GBP", "SEK", "NOK", "DKK", "CHF", "JPY"}
MIN_REPORTABLE_NOTIONAL = 10_000.0


def validate_trade(trade: Trade) -> tuple[bool, str | None]:
    """
    Validates a trade against EMIR-style reporting rules.
    Returns (is_valid, error_message)
    """

    # 1. LEI must be exactly 20 characters (alphanumeric)
    if not trade.counterparty_lei.isalnum() or len(trade.counterparty_lei) != 20:
        return False, "Invalid LEI: must be 20 alphanumeric characters"

    # 2. Notional must be above reporting threshold
    if trade.notional < MIN_REPORTABLE_NOTIONAL:
        return False, f"Notional {trade.notional} is below reporting threshold of {MIN_REPORTABLE_NOTIONAL}"

    # 3. Currency must be valid ISO 4217
    if trade.currency not in VALID_CURRENCIES:
        return False, f"Currency '{trade.currency}' is not accepted for regulatory reporting"

    # 4. Settlement date must be after trade date
    if trade.settlement_date <= trade.trade_date:
        return False, "Settlement date must be after trade date"

    # 5. Trade date cannot be in the future
    if trade.trade_date > datetime.now():
        return False, "Trade date cannot be in the future"

    return True, None


def apply_validation(trade: Trade) -> Trade:
    is_valid, error = validate_trade(trade)

    if is_valid:
        trade.status = TradeStatus.VALIDATED
        trade.validation_error = None
    else:
        trade.status = TradeStatus.FAILED
        trade.validation_error = error

    return trade