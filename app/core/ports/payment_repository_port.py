from abc import ABC, abstractmethod
from typing import Optional
from app.core.entities.payment import Payment

class PaymentRepositoryPort(ABC):
    @abstractmethod
    def create(self, payment: Payment) -> Payment:
        """Cria um pagamento e retorna a entidade Payment com o ID gerado."""
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        """Retorna o pagamento associado ao ID do pedido ou None se não existir."""
        pass

    @abstractmethod
    def update(self, payment: Payment) -> Payment:
        """Atualiza um pagamento existente e retorna a entidade atualizada."""
        pass
