from fastapi import APIRouter, HTTPException
from app.schemas import TransactionInput, TransactionOutput
import joblib
import os
import pandas as pd
from app.database import SessionLocal, Transaction

router = APIRouter()

MODEL_PATH = "app/models/aml_model.pkl"
ENC_PATH = "app/models/country_encoder.pkl"

# Make sure model exists; if not, throw helpful error
if not os.path.exists(MODEL_PATH) or not os.path.exists(ENC_PATH):
    raise RuntimeError("Model files not found. Run `python app/models/train_model.py` to generate them.")

model = joblib.load(MODEL_PATH)
le = joblib.load(ENC_PATH)

@router.post("/score", response_model=TransactionOutput)
def score_transaction(tx: TransactionInput):
    # encode country safely (handle unseen countries)
    try:
        country_enc = le.transform([tx.counterparty_country])[0]
    except Exception:
        # unseen country -> append and transform fallback by mapping to -1
        # but LabelEncoder can't transform unseen, so map to a default (like 0)
        country_enc = 0

    X = pd.DataFrame([[tx.amount, country_enc, int(tx.is_international)]],
                     columns=["amount","country_enc","is_international"])
    # If model expects different names it's fine: we trained similarly
    try:
        risk_prob = float(model.predict_proba(X)[0][1])
    except Exception:
        # if model doesn't have predict_proba fallback to predict
        risk_prob = float(model.predict(X)[0])

    label = "Normal"
    reasons = []
    if risk_prob >= 0.8 or tx.amount > 50000:
        label = "Suspicious"
        reasons.append("High risk probability or large amount")
    elif risk_prob >= 0.5:
        label = "Medium"
        reasons.append("Medium risk probability")

    if tx.is_international:
        reasons.append("International transfer")
    if tx.counterparty_country == "KY":
        reasons.append("High-risk counterparty country (KY)")

    # store in DB
    db = SessionLocal()
    db_tx = Transaction(
        transaction_id=tx.transaction_id,
        customer_id=tx.customer_id,
        amount=tx.amount,
        counterparty_country=tx.counterparty_country,
        is_international=tx.is_international,
        risk_score=risk_prob,
        label=label,
        reasons=",".join(reasons)
    )
    db.add(db_tx)
    try:
        db.commit()
    except Exception:
        db.rollback()
    db.refresh(db_tx)
    db.close()

    return TransactionOutput(
        transaction_id=tx.transaction_id,
        amount=tx.amount,
        risk_score=risk_prob,
        label=label,
        reasons=reasons
    )
