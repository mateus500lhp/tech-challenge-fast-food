from dataclasses import dataclass
from typing import Optional

@dataclass
class OrderItem:
    id: Optional[int]
    order_id: int
    product_id: int
    quantity: int
    price: float
