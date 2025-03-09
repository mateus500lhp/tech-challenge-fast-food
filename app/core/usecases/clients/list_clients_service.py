from typing import List
from app.core.entities.client import Client
from app.core.ports.client_repository_port import ClientRepositoryPort

class ListClientsService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository

    def execute(self) -> List[Client]:
        """
        Busca todos os clientes no repositório e os retorna.
        """
        return self.client_repository.find_all()
