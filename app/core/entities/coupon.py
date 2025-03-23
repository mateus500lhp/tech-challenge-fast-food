from datetime import date
from dataclasses import dataclass
from typing import Optional

@dataclass
class Coupon:
    hash: Optional[str]
    descricao: Optional[str]
    discount_percentage: float
    max_discount: float
    expires_at: Optional[date]
    active: bool = True
    id: Optional[int] = None
