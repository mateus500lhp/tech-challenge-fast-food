from datetime import date
from pydantic import BaseModel


class CouponIn(BaseModel):
    discount_percentage: float
    max_discount: float
    expires_at: date
    descricao: str
    hash: str

class CouponUpdateIn(BaseModel):
    discount_percentage: float
    max_discount: float
    expires_at: date
    descricao: str
    hash: str
    active: bool

class CouponOut(BaseModel):
    hash: str
    descricao: str
    discount_percentage: float
    max_discount: float
    expires_at: date
    active: bool