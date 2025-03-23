from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.shared.enums.payment_status import PaymentStatus


class PaymentStatusResponse(BaseModel):
    order_id: int
    payment_status: str
    qr_code: Optional[str] = None
    description: Optional[str] = ""
    payment_date: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True

class PaymentQRCode(BaseModel):
    qr_data: str

class PaymentWebhookRequest(BaseModel):
    order_id: int
    payment_status: PaymentStatus
    description: Optional[str] = None
