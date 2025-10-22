from fastapi import APIRouter
from app.database import SessionLocal, Transaction

router = APIRouter()

@router.get("/alerts")
def get_alerts(limit: int = 50):
    db = SessionLocal()
    txs = db.query(Transaction).filter(Transaction.label != "Normal").order_by(Transaction.risk_score.desc()).limit(limit).all()
    alerts = []
    for tx in txs:
        alerts.append({
            "transaction_id": tx.transaction_id,
            "customer_id": tx.customer_id,
            "amount": tx.amount,
            "counterparty_country": tx.counterparty_country,
            "is_international": tx.is_international,
            "risk_score": tx.risk_score,
            "label": tx.label,
            "reasons": tx.reasons.split(",") if tx.reasons else []
        })
    db.close()
    return {"alerts": alerts}
