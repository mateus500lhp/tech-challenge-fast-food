from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.adapters.dependencies.auth import get_current_user
from app.adapters.gateways.coupon import CouponRepository
from app.adapters.gateways.order import OrderRepository
from app.adapters.gateways.payment import PaymentRepository
from app.adapters.gateways.product import ProductRepository
from app.adapters.presenters.order.order_presenter import OrderPresenter
from app.core.schemas.order_schemas import OrderIn, OrderOut
from app.core.schemas.payment_schemas import PaymentStatusResponse
from app.core.usecases.orders.create_order_service import CreateOrderService
from app.core.usecases.orders.list_order_service import ListOrdersService, GetOrderByIdService, \
    ListOrdersByStatusService, ListOrdersByClientService
from app.core.usecases.orders.update_order_service import UpdateOrderStatusService
from app.core.usecases.payment.create_payment_service import PaymentService
from app.core.usecases.payment.get_payment_status_service import GetPaymentStatusService
from app.devices.db.connection import get_db_session
from app.shared.enums.order_status import OrderStatus

router = APIRouter()

@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(
    order_in: OrderIn,
    db: Session = Depends(get_db_session),
    user: Optional[dict] = Depends(get_current_user)
):
    """Cria um novo pedido"""
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)
    coupon_repo = CouponRepository(db)
    payment_repo = PaymentRepository(db)
    service = CreateOrderService(order_repo, product_repo, coupon_repo)
    payment_service = PaymentService(payment_repo)
    client_id = None if user is None else user["user_id"]
    try:
        order = service.execute(order_in, client_id=client_id)
        _ = payment_service.execute(order)
        return OrderPresenter.present(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db_session)):
    """Lista todos os pedidos"""
    service = ListOrdersService(OrderRepository(db))
    return OrderPresenter.present_list(service.execute())

@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db_session)):
    """Busca um pedido pelo ID"""
    service = GetOrderByIdService(OrderRepository(db))
    order = service.execute(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderPresenter.present(order)

@router.get("/orders/status/{status}", response_model=List[OrderOut])
def list_orders_by_status(status: OrderStatus, db: Session = Depends(get_db_session)):
    """Lista pedidos por status"""
    service = ListOrdersByStatusService(OrderRepository(db))
    return OrderPresenter.present_list(service.execute(status))

@router.get("/orders/client/{client_id}", response_model=List[OrderOut])
def list_orders_by_client(client_id: int, db: Session = Depends(get_db_session)):
    """Lista pedidos de um cliente específico"""
    service = ListOrdersByClientService(OrderRepository(db))
    return OrderPresenter.present_list(service.execute(client_id))


@router.patch("/orders/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    db: Session = Depends(get_db_session)
):
    service = UpdateOrderStatusService(OrderRepository(db),PaymentRepository(db))
    try:
        updated_order = service.execute(order_id, new_status)
        return OrderPresenter.present(updated_order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{order_id}/payment_status")
def get_payment_status(order_id: int, db: Session = Depends(get_db_session)):
    """
    Retorna o status de pagamento do pedido informado.
    """
    payment_repo = PaymentRepository(db)
    service = GetPaymentStatusService(payment_repo)
    try:
        payment = service.execute(order_id)
        return PaymentStatusResponse(
            order_id=payment.order_id,
            payment_status=payment.status,
            qr_code=payment.qr_code,
            amount=payment.amount,
            payment_date=payment.payment_date,
            description=payment.description,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))