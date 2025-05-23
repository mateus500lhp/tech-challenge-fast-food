from sqlalchemy import case, asc
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.entities.item import OrderItem
from app.core.entities.order import Order
from app.core.ports.order_repository_port import OrderRepositoryPort
from app.devices.db.models import OrderModel, OrderItemModel
from app.shared.enums.order_status import OrderStatus


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

    def find_by_id(self, order_id: int) -> Optional[Order]:
        order_model = (
            self.db_session.query(OrderModel)
            .filter(OrderModel.id == order_id)
            .filter(OrderModel.active == True)
            .first()
        )
        if not order_model:
            return None

        return Order(
            id=order_model.id,
            client_id=order_model.client_id,
            status=order_model.status,
            coupon_id=order_model.coupon_id,
            amount=order_model.amount,
            items=[
                OrderItem(
                    id=item.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                    name=getattr(item.product, "name", "Unknown"),
                )
                for item in order_model.items
            ]
        )

    def find_all(self) -> List[Order]:
        order_models = (
            self.db_session.query(OrderModel)
            .filter(OrderModel.active == True)
            .all()
        )

        return [
            Order(
                id=order_model.id,
                client_id=order_model.client_id,
                status=order_model.status,
                coupon_id=order_model.coupon_id,
                amount=order_model.amount,
                items=[
                    OrderItem(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        name=getattr(item.product, "name", "Unknown"),
                    )
                    for item in order_model.items
                ]
            )
            for order_model in order_models
        ]

    def find_by_status(self, status: str) -> List[Order]:
        order_models = (
            self.db_session.query(OrderModel)
            .filter(OrderModel.status == status)
            .filter(OrderModel.active == True)
            .all()
        )

        return [
            Order(
                id=order_model.id,
                client_id=order_model.client_id,
                status=order_model.status,
                coupon_id=order_model.coupon_id,
                amount=order_model.amount,
                items=[
                    OrderItem(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        name=getattr(item.product, "name", "Unknown"),
                    )
                    for item in order_model.items
                ]
            )
            for order_model in order_models
        ]

    def find_by_client(self, client_id: int) -> List[Order]:
        order_models = (
            self.db_session.query(OrderModel)
            .filter(OrderModel.client_id == client_id)
            .filter(OrderModel.active == True)
            .all()
        )

        return [
            Order(
                id=order_model.id,
                client_id=order_model.client_id,
                status=order_model.status,
                coupon_id=order_model.coupon_id,
                amount=order_model.amount,
                items=[
                    OrderItem(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        name=getattr(item.product, "name", "Unknown"),
                    )
                    for item in order_model.items
                ]
            )
            for order_model in order_models
        ]

    def find_active_sorted_orders(self) -> List[Order]:
        """
        Retorna os pedidos que não estão 'Finalizados' e ordena:
         1. Pronto > Em Preparação > Recebido;
         2. Pedidos mais antigos (pelo id) primeiro.
        """
        status_priority = case(
            (OrderModel.status == OrderStatus.READY, 1),
            (OrderModel.status == OrderStatus.IN_PROGRESS, 2),
            (OrderModel.status == OrderStatus.RECEIVED, 3),
            else_=9999
        )

        order_models = (
            self.db_session.query(OrderModel)
            .filter(OrderModel.status != OrderStatus.COMPLETED)
            .filter(OrderModel.active == True)
            .order_by(status_priority, asc(OrderModel.id))
            .all()
        )

        return [
            Order(
                id=order_model.id,
                client_id=order_model.client_id,
                status=order_model.status,
                coupon_id=order_model.coupon_id,
                amount=order_model.amount,
                items=[
                    OrderItem(
                        id=item.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                        name=getattr(item.product, "name", "Unknown"),
                    )
                    for item in order_model.items
                ]
            )
            for order_model in order_models
        ]

    def update(self, order: Order) -> Order:
        # Busca o modelo do pedido no banco pelo ID
        order_model = self.db_session.query(OrderModel).get(order.id)
        if not order_model:
            raise ValueError("Pedido não encontrado.")

        # Atualiza o status do pedido
        order_model.status = order.status

        self.db_session.commit()
        self.db_session.refresh(order_model)

        updated_items = [
            OrderItem(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
                name=getattr(item.product, "name", "Unknown"),
            )
            for item in order_model.items
        ]

        return Order(
            id=order_model.id,
            client_id=order_model.client_id,
            status=order_model.status,
            coupon_id=order_model.coupon_id,
            amount=order_model.amount,
            items=updated_items,
        )

    def delete(self, order_id: int) -> None:
        """Remove o order pelo ID."""
        pass