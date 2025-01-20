from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.adapters.driven.repositories.order import OrderRepository
from app.adapters.driven.repositories.product import ProductRepository
from app.domain.entities.item import OrderItem
from app.domain.entities.order import Order
from app.domain.services.orders.create_order_service import CreateOrderService
from app.shared.enums.order_status import OrderStatus
from database import get_db_session

router = APIRouter()

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderIn(BaseModel):
    client_id: Optional[int] = None
    coupon_id: Optional[int] = None
    items: List[OrderItemIn]


class OrderItemOut(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float


class OrderOut(BaseModel):
    id: int
    client_id: Optional[int]
    coupon_id: Optional[int]
    status: OrderStatus
    items: List[OrderItemOut]
    amount: float

@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order_in: OrderIn, db: Session = Depends(get_db_session)):
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)
    service = CreateOrderService(order_repo, product_repo)

    # Converte OrderIn -> Domain Model
    order = Order(
        client_id=order_in.client_id,
        coupon_id=order_in.coupon_id,
        status=OrderStatus.RECEIVED,
        items=[
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
            )
            for item in order_in.items
        ],
    )

    try:
        created_order = service.execute(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Converte o resultado para Pydantic
    return OrderOut(
        id=created_order.id,
        client_id=created_order.client_id,
        coupon_id=created_order.coupon_id,
        status=created_order.status,
        items=[
            OrderItemOut(
                product_id=item.product_id,
                name=item.name,
                quantity=item.quantity,
                price=item.price,
            )
            for item in created_order.items
        ],
        amount=created_order.amount,
    )