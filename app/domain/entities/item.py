from dataclasses import dataclass
from typing import Optional

@dataclass
class OrderItem:
    id: Optional[int] = None
    product_id: int = 0
    quantity: int = 1
    price: Optional[float] = 0.0
    name: Optional[str] = None
