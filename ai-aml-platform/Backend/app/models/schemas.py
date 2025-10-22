from pydantic import BaseModel
from typing import List

class TransactionInput(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    counterparty_country: str
    is_international: bool

class TransactionOutput(BaseModel):
    transaction_id: str
    amount: float
    risk_score: float
    label: str
    reasons: List[str]
