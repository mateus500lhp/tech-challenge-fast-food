import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Coupon:
    id: Optional[int]
    hash: str
    discount_percentage: float
    max_discount: float
    active: bool = True
    expires_at: Optional[datetime] = None