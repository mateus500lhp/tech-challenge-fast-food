from dataclasses import dataclass, field
from typing import Optional, List
# from app.shared.enums.order_status import OrderStatus

@dataclass
class Order:
    id: Optional[int]
    client_id: int
    status: str
    coupon_id: Optional[int] = None
    # items: List["OrderItem"] = field(default_factory=list)  # Lista de itens
    # payment: Optional["Payment"] = None
