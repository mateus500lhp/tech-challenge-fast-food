from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from app.shared.enums.payment_status import PaymentStatus

@dataclass
class Payment:
    id: Optional[int]
    order_id: int
    qr_code: Optional[str] = None
    status: PaymentStatus = PaymentStatus.PENDING
    payment_date: Optional[datetime] = None
    description: Optional[str] = None
    amount: float = 0.0
