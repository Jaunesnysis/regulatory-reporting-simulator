from fastapi import FastAPI
from app.routers import trades, reports, health
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Regulatory Reporting Simulator",
    description="EMIR/MiFID II trade reporting pipeline simulator",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(trades.router)
app.include_router(reports.router)