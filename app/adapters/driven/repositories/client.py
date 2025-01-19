from typing import List, Optional
from sqlalchemy.orm import Session

from app.adapters.driven.models.client import ClientModel
from app.domain.entities.client import Client
from app.domain.ports.client_repository_port import ClientRepositoryPort


class ClientRepository(ClientRepositoryPort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, client: Client) -> Client:
        """
        Cria um novo cliente no banco de dados a partir de uma instância de domínio.
        """
        client_model = ClientModel(
            name=client.name,
            email=client.email,
            cpf=client.cpf,
            password=client.password,
        )
        self.db_session.add(client_model)
        self.db_session.commit()
        self.db_session.refresh(client_model)

        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
        )

    def find_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca um cliente pelo ID. Retorna None se não encontrado.
        """
        client_model = self.db_session.query(ClientModel).get(client_id)
        if not client_model:
            return None

        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
        )

    def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente pelo CPF. Retorna None se não encontrado.
        """
        client_model = (
            self.db_session.query(ClientModel).filter(ClientModel.cpf == cpf).first()
        )
        if not client_model:
            return None

        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
            created_at=client_model.created_at,
            updated_at=client_model.updated_at,
        )
    def find_by_email(self, email: str) -> Optional[Client]:
        """
        Busca um cliente pelo email. Retorna None se não encontrado.
        """
        client_model = (
            self.db_session.query(ClientModel).filter(ClientModel.email == email).first()
        )
        if not client_model:
            return None

        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
            created_at=client_model.created_at,
            updated_at=client_model.updated_at,
        )

    def find_all(self) -> List[Client]:
        """
        Retorna todos os clientes do banco de dados.
        """
        client_models = self.db_session.query(ClientModel).all()
        return [
            Client(
                id=m.id,
                name=m.name,
                email=m.email,
                cpf=m.formatted_cpf,
                password=m.password,
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in client_models
        ]

    def update(self, client: Client) -> Client:
        """
        Atualiza um cliente existente no banco de dados.
        """
        client_model = self.db_session.query(ClientModel).get(client.id)
        if not client_model:
            raise ValueError("Client not found")

        client_model.name = client.name
        client_model.email = client.email
        client_model.cpf = client.cpf
        client_model.password = client.password

        self.db_session.commit()
        self.db_session.refresh(client_model)

        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
        )

    def delete(self, client_id: int) -> None:
        """
        Deleta um cliente pelo ID.
        """
        client_model = self.db_session.query(ClientModel).get(client_id)
        if client_model:
            self.db_session.delete(client_model)
            self.db_session.commit()

    def inactivate(self, client_id: int) -> Optional[Client]:
        """
        Marca o cliente como inativo (active = False).
        Retorna o Client se encontrado, ou None se não encontrado.
        """
        client_model = self.db_session.query(ClientModel).get(client_id)
        if not client_model:
            return None  # ou poderia lançar um ValueError se preferir

        client_model.active = False
        self.db_session.commit()
        self.db_session.refresh(client_model)

        # Retorna a entidade de domínio com active=False
        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
            active=client_model.active
        )
