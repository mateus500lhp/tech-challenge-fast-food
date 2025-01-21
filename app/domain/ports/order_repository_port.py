from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.order import Order

class OrderRepositoryPort(ABC):

    """Define a interface (porta) para persistência de Order."""

    @abstractmethod
    def create(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        """Retorna um Order (ou None se não encontrado)."""
        pass

    @abstractmethod
    def find_all(self) -> List[Order]:
        """Lista todos os orders."""
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        """Atualiza um order existente."""
        pass

    @abstractmethod
    def delete(self, order_id: int) -> None:
        """Remove o order pelo ID."""
        pass