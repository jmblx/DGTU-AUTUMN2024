# models/external_models.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional


class ReceiptItem(BaseModel):
    name: str
    count: float
    price: float


class Receipt(BaseModel):
    id: str
    time: str  # Возможно, лучше использовать datetime, но в текущей спецификации это строка
    items: List[ReceiptItem]
    total_price: float


class Purchaser(BaseModel):
    id: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    access: bool
    confirmation_code: Optional[str] = None
    code_expiry: Optional[int] = None  # Unixtime
    receipts: List[Receipt] = []
