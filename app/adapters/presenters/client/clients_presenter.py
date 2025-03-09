from typing import List

from app.adapters.presenters.client.client_presenter import ClientPresenter
from app.core.entities.client import Client
from app.core.schemas.client_schemas import ClientsOut

class ClientsPresenter:
    @staticmethod
    def present(clients: List[Client]) -> List[ClientsOut]:
        """
        Converte uma lista de entidades `Client` para `ClientsOut`, formatando os CPFs.
        """
        return [
            ClientsOut(
                id=client.id,
                name=client.name,
                email=client.email,
                cpf=ClientPresenter.format_cpf(client.cpf),
                active=client.active,
                created_at=client.created_at,
                updated_at=client.updated_at,
            )
            for client in clients
        ]
