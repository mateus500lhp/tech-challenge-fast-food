# app/core/ports/product_repository_port.py
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.product import Product


class ProductRepositoryPort(ABC):
    """Define a interface (porta) para persistência de Product."""

    @abstractmethod
    def create(self, product: Product) -> Product:
        """Cria um novo product no repositório e retorna com ID populado."""
        pass

    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Retorna um Product (ou None se não encontrado)."""
        pass

    @abstractmethod
    def find_all(self) -> List[Product]:
        """Lista todos os products."""
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        """Atualiza um product existente."""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> None:
        """Remove o product pelo ID."""
        pass
