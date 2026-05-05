from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeResponse
from app.services.validator import apply_validation
from typing import List
import uuid

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.post("/", response_model=TradeResponse)
def submit_trade(trade_in: TradeCreate, db: Session = Depends(get_db)):
    """Submit a new trade for validation and regulatory reporting."""

    existing = db.query(Trade).filter(Trade.trade_ref == trade_in.trade_ref).first()
    if existing:
        raise HTTPException(status_code=400, detail="Trade with this reference already exists")

    trade = Trade(
        id=uuid.uuid4(),
        **trade_in.model_dump()
    )

    trade = apply_validation(trade)

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return trade


@router.get("/", response_model=List[TradeResponse])
def get_trades(db: Session = Depends(get_db)):
    """Get all submitted trades."""
    return db.query(Trade).all()


@router.get("/{trade_ref}", response_model=TradeResponse)
def get_trade(trade_ref: str, db: Session = Depends(get_db)):
    """Get a single trade by reference."""
    trade = db.query(Trade).filter(Trade.trade_ref == trade_ref).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade