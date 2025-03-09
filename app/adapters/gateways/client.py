from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.entities.client import Client
from app.core.ports.client_repository_port import ClientRepositoryPort
from app.devices.db.models import ClientModel, CouponModel, ClientCouponAssociationModel


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
            password=client_model.password
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
            active=client_model.active,
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
            user_type=client_model.user_type,
            active=client_model.active,
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
            active=client_model.active,
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
                active=m.active,
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
        client_model.active = client.active

        self.db_session.commit()
        self.db_session.refresh(client_model)

        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            cpf=client_model.cpf,
            password=client_model.password,
            created_at=client_model.created_at,
            updated_at=client_model.updated_at,
            active=client_model.active,
        )

    def delete(self, client_id: int) -> None:
        """
        Deleta um cliente pelo ID.
        """
        client_model = self.db_session.query(ClientModel).get(client_id)
        if client_model:
            self.db_session.delete(client_model)
            self.db_session.commit()

    def find_coupons_by_client_id(self, client_id: int):
        """
        Retorna todos os cupons ativos e não expirados vinculados a um cliente.
        Considera a flag VIP para restringir os cupons a certos clientes.

        :param client_id: ID do cliente
        :return: Lista de cupons não expirados e ativos
        """
        current_date = datetime.utcnow()

        coupons = (
            self.db_session.query(CouponModel)
            .outerjoin(ClientCouponAssociationModel, CouponModel.id == ClientCouponAssociationModel.coupon_id)
            .filter(
                # Cupons ativos
                CouponModel.active == True,
                # Cupons não expirados
                CouponModel.expires_at >= current_date,
                # Se VIP, verificar associação com o cliente
                ((CouponModel.vip == True) & (ClientCouponAssociationModel.client_id == client_id))
                | (CouponModel.vip == False)  # Se não VIP, é para todos
            )
            .all()
        )

        return coupons

