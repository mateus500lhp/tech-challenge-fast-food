from datetime import datetime
from pydantic import BaseModel

class CouponOut(BaseModel):
    hash: str
    discount_percentage: float
    max_discount: float
    expires_at: datetime