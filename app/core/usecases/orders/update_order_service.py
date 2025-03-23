from typing import Optional
from app.core.entities.order import Order
from app.core.ports.order_repository_port import OrderRepositoryPort
from app.core.ports.payment_repository_port import PaymentRepositoryPort
from app.shared.enums.order_status import OrderStatus
from app.shared.enums.payment_status import PaymentStatus


class UpdateOrderStatusService:
    def __init__(self, order_repository: OrderRepositoryPort,payment_repository: PaymentRepositoryPort):
        self.order_repository = order_repository
        self.payment_repository = payment_repository

    def execute(self, order_id: int, new_status: OrderStatus) -> Order:
        # Busca o pedido atual
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido não encontrado.")

        if new_status != OrderStatus.RECEIVED:
            payment = self.payment_repository.get_by_order_id(order_id)
            if not payment or payment.status != PaymentStatus.PAID:
                raise ValueError(
                    "Não é possível alterar o status para diferente de RECEIVED sem que o pagamento esteja aprovado."
                )

        # Atualiza o status (pode incluir validações adicionais se necessário)
        order.status = new_status

        # Persiste a alteração e retorna o pedido atualizado
        return self.order_repository.update(order)
