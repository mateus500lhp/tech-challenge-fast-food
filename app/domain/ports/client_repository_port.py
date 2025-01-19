from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.client import Client


class ClientRepositoryPort(ABC):
    """Define a interface (porta) para persistência de Client."""

    @abstractmethod
    def create(self, client: Client) -> Client:
        """Cria um novo Client no repositório e retorna com ID populado."""
        pass

    @abstractmethod
    def find_by_id(self, client_id: int) -> Optional[Client]:
        """Retorna um Client (ou None se não encontrado)."""
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """Retorna um Client (ou None se não encontrado) pelo CPF."""
        pass
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Client]:
        """Retorna um Client (ou None se não encontrado) pelo Email."""
        pass

    @abstractmethod
    def find_all(self) -> List[Client]:
        """Lista todos os Clients."""
        pass

    @abstractmethod
    def update(self, client: Client) -> Client:
        """Atualiza um Client existente."""
        pass

    @abstractmethod
    def delete(self, client_id: int) -> None:
        """Remove o Client pelo ID (exclusão física)."""
        pass

    @abstractmethod
    def inactivate(self, client_id: int) -> Optional[Client]:
        """
        Marca o Client como inativo (active=False).
        Retorna o Client atualizado ou None se não encontrado.
        """
        pass
