from dataclasses import dataclass
from typing import Optional

@dataclass
class OrderItem:
    id: Optional[int] = None
    product_id: int = 0
    quantity: int = 1
    price: Optional[float] = 0.0
    name: Optional[str] = None

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("A quantidade do item deve ser maior que zero.")
        if self.price < 0:
            raise ValueError("O preço deve ser maior que zero.")