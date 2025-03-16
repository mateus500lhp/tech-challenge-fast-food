from typing import Optional
from app.core.entities.order import Order
from app.core.ports.order_repository_port import OrderRepositoryPort
from app.shared.enums.order_status import OrderStatus


class UpdateOrderStatusService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.order_repository = order_repository

    def execute(self, order_id: int, new_status: OrderStatus) -> Order:
        # Busca o pedido atual
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido não encontrado.")

        # Atualiza o status (pode incluir validações adicionais se necessário)
        order.status = new_status

        # Persiste a alteração e retorna o pedido atualizado
        return self.order_repository.update(order)
