from typing import List
from app.domain.entities.client import Client
from app.domain.ports.client_repository_port import ClientRepositoryPort

class ListClientsService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository

    def execute(self) -> List[Client]:
        # Busca todos os clientes no repositório
        clients = self.client_repository.find_all()
        return clients
