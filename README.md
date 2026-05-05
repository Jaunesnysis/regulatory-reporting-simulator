# Regulatory Reporting Simulator

A backend API simulating a financial trade regulatory reporting pipeline, modelled after real-world **EMIR** and **MiFID II** compliance workflows used by banks and financial institutions across Europe.

Built with **Python**, **FastAPI**, and **PostgreSQL**.

---

## What It Does

Financial institutions are legally required to report every trade to regulators within strict deadlines. This system simulates that end-to-end pipeline:

1. **Trade Ingestion** — accepts trades via REST API (FX, Bonds, Interest Rate Swaps)
2. **Validation** — checks LEI codes, notional thresholds, currency eligibility, settlement dates
3. **Enrichment** — classifies asset class, calculates reporting deadline, assigns regulation
4. **Report Generation** — produces structured CSV reports ready for regulatory submission
5. **Audit Trail** — every trade stored with status (VALIDATED / FAILED / REPORTED) and failure reason

---

## Tech Stack

| Layer          | Technology    |
| -------------- | ------------- |
| API            | FastAPI       |
| Database       | PostgreSQL 15 |
| ORM            | SQLAlchemy    |
| Validation     | Pydantic v2   |
| Infrastructure | Docker        |
| Language       | Python 3.9+   |

---

## Project Structure

app/
├── models/ # SQLAlchemy ORM models (Trade, Report)
├── schemas/ # Pydantic request/response schemas
├── routers/ # FastAPI endpoints
├── services/ # Business logic (validator, enricher, report generator)
└── reports/ # CSV/XML exporters

---

## Regulatory Rules Implemented

- **LEI Validation** — Legal Entity Identifier must be exactly 20 alphanumeric characters
- **Notional Threshold** — trades below €10,000 are flagged and excluded from reporting
- **Currency Eligibility** — only accepted ISO 4217 currencies (EUR, USD, GBP, SEK, NOK, DKK, CHF, JPY)
- **Settlement Date Logic** — settlement must be after trade date
- **Reporting Deadline** — calculated automatically from trade date (T+1 per EMIR)
- **Asset Class Classification** — FX, Rates, Credit, Equity

---

## Supported Instruments

- FX Spot
- FX Forward
- Interest Rate Swap
- Bond
- Equity

---

## Getting Started

### Prerequisites

- Docker
- Python 3.9+

### Run locally

```bash
# Start PostgreSQL
docker-compose up -d

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint              | Description                   |
| ------ | --------------------- | ----------------------------- |
| GET    | `/health`             | Service health check          |
| POST   | `/trades/`            | Submit a trade for validation |
| GET    | `/trades/`            | Get all trades                |
| GET    | `/trades/{trade_ref}` | Get trade by reference        |
| POST   | `/reports/generate`   | Generate EMIR CSV report      |
| GET    | `/reports/`           | Get all generated reports     |

---

## Example Trade Submission

```json
{
  "trade_ref": "TRD-20240501-001",
  "counterparty_lei": "SWEDSESS00LEI000001X",
  "instrument_type": "FX_SPOT",
  "notional": 1500000.0,
  "currency": "EUR",
  "trade_date": "2024-05-01T10:00:00",
  "settlement_date": "2024-05-03T10:00:00",
  "venue": "XSTO"
}
```

### Validated response

```json
{
  "trade_ref": "TRD-20240501-001",
  "status": "VALIDATED",
  "validation_error": null
}
```

### Failed response (below notional threshold)

```json
{
  "trade_ref": "TRD-20240501-002",
  "status": "FAILED",
  "validation_error": "Notional 500.0 is below reporting threshold of 10000.0"
}
```

---

## Generated Report (CSV)

trade_ref,counterparty_lei,instrument_type,asset_class,notional,currency,trade_date,settlement_date,venue,reporting_deadline,regulation,report_status
TRD-20240501-001,SWEDSESS00LEI000001X,FX_SPOT,Foreign Exchange,1500000.0,EUR,2024-05-01,2024-05-03,XSTO,2024-05-02,EMIR,PENDING_SUBMISSION

---
