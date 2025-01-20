from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.coupon import Coupon


class CouponRepositoryPort(ABC):
    """Define a interface (porta) para persistência de Coupon."""

    @abstractmethod
    def create(self, coupon: Coupon) -> Coupon:
        """Cria um novo Coupon no repositório e retorna com ID populado."""
        pass

    @abstractmethod
    def find_by_hash(self, coupon_hash: str) -> Optional[Coupon]:
        """Retorna um Coupon (ou None se não encontrado) pelo hash único."""
        pass

    @abstractmethod
    def find_all(self) -> List[Coupon]:
        """Lista todos os Coupons cadastrados."""
        pass

    @abstractmethod
    def update(self, coupon: Coupon) -> Coupon:
        """Atualiza um Coupon existente."""
        pass

    @abstractmethod
    def delete(self, coupon_id: int) -> None:
        """Remove o Coupon pelo ID (exclusão física)."""
        pass
