from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.adapters.driven.repositories.coupon import CouponRepository
from app.adapters.driven.repositories.order import OrderRepository
from app.adapters.driven.repositories.product import ProductRepository
from app.adapters.driver.controllers.order.order_schemas import OrderIn, OrderOut, OrderItemOut
from app.adapters.driver.dependencias.auth import get_current_user
from app.domain.entities.item import OrderItem
from app.domain.entities.order import Order
from app.domain.services.orders.create_order_service import CreateOrderService
from app.domain.services.orders.list_order_service import ListOrdersService, ListOrdersByStatusService
from app.shared.enums.order_status import OrderStatus
from database import get_db_session

router = APIRouter()

@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(
    order_in: OrderIn,
    db: Session = Depends(get_db_session),
    user: Optional[dict] = Depends(get_current_user)
):
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)
    coupon_repo = CouponRepository(db)
    service = CreateOrderService(order_repo, product_repo,coupon_repo)

    # Converte OrderIn -> Domain Model
    order = Order(
        client_id= None if user is None else user["user_id"],
        coupon_hash=order_in.coupon_hash,
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
        coupon_hash=order_in.coupon_hash,
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


@router.get("/orders", response_model=List[OrderOut], status_code=200)
def list_orders(
    db: Session = Depends(get_db_session),
    user: Optional[dict] = Depends(get_current_user),
):
    repo = OrderRepository(db)
    use_case = ListOrdersService(repo)

    orders = use_case.execute()

    return [
        OrderOut(
            id=order.id,
            client_id=order.client_id,
            coupon_hash=order.coupon_id,
            status=order.status,
            items=[
                OrderItemOut(
                    product_id=item.product_id,
                    name=item.name,
                    quantity=item.quantity,
                    price=item.price,
                )
                for item in order.items
            ],
            amount=order.amount,
        )
        for order in orders
    ]

@router.get("/orders/status/{status}", response_model=List[OrderOut], status_code=200)
def list_orders_by_status(
    status: OrderStatus,
    db: Session = Depends(get_db_session),
    user: Optional[dict] = Depends(get_current_user),
):
    order_repo = OrderRepository(db)
    service = ListOrdersByStatusService(order_repo)

    orders = service.execute(status)

    return [
        OrderOut(
            id=order.id,
            client_id=order.client_id,
            coupon_hash=order.coupon_id,
            status=order.status,
            items=[
                OrderItemOut(
                    product_id=item.product_id,
                    name=item.name,
                    quantity=item.quantity,
                    price=item.price,
                )
                for item in order.items
            ],
            amount=order.amount,
        )
        for order in orders
    ]

