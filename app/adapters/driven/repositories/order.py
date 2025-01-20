from sqlalchemy.orm import Session
from typing import Optional, List

from app.adapters.driven.models import OrderModel, OrderItemModel
from app.domain.entities.item import OrderItem
from app.domain.entities.order import Order
from app.domain.ports.order_repository_port import OrderRepositoryPort

class OrderRepository(OrderRepositoryPort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, order: Order) -> Order:
        order_model = OrderModel(
            client_id=order.client_id,
            status=order.status,
            coupon_id=order.coupon_id,
            amount=order.amount,
        )
        self.db_session.add(order_model)
        self.db_session.flush()

        # Criação de itens do pedido com preço incluído
        order_item_models = []
        for item in order.items:
            item_model = OrderItemModel(
                order_id=order_model.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            self.db_session.add(item_model)
            order_item_models.append(item_model)

        self.db_session.commit()

        # Atualiza os objetos criados
        self.db_session.refresh(order_model)
        for item_model in order_item_models:
            self.db_session.refresh(item_model)

        created_items = [
            OrderItem(
                id=item_model.id,
                product_id=item_model.product_id,
                quantity=item_model.quantity,
                price=item_model.price,
            )
            for item_model in order_item_models
        ]

        return Order(
            id=order_model.id,
            client_id=order_model.client_id,
            status=order_model.status,
            coupon_id=order_model.coupon_id,
            amount=order_model.amount,
            items=created_items,
        )