from app.domain.entities.client import Client
from app.domain.ports.client_repository_port import ClientRepositoryPort
from app.domain.entities.coupon import Coupon
from app.shared.handles.jwt_user import create_access_token
from app.shared.validates.cpf_validate import is_cpf_valid



class IdentifyClientService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository

    def normalize_and_validate_cpf(self, cpf: str) -> str:
        """
        Remove formatações do CPF e realiza validações básicas.
        """
        digits = "".join(c for c in cpf if c.isdigit())
        if len(digits) != 11 or not is_cpf_valid(digits):
            raise ValueError("CPF inválido.")
        return digits

    def execute(self, cpf: str) -> dict:
        """
        Identifica o cliente pelo CPF, retorna o cliente com cupons vinculados e um JWT.

        Args:
            cpf (str): CPF do cliente.

        Returns:
            dict: Contém os dados do cliente, cupons vinculados e um JWT.
        """
        # 1) Normalizar e validar o CPF
        clean_cpf = self.normalize_and_validate_cpf(cpf)

        # 2) Buscar cliente no repositório
        client = self.client_repository.find_by_cpf(clean_cpf)
        if not client:
            raise ValueError("CPF não encontrado no sistema.")

        if not client.active:
            raise ValueError("CPF inativado no sistema.")

        # 3) Buscar cupons vinculados ao cliente
        coupons = self.client_repository.find_coupons_by_client_id(client.id)

        # 4) Gerar JWT para o cliente
        jwt_token = create_access_token({
            "id": client.id,
            "cpf": client.cpf,
            "email": client.email,
            "name": client.name,
            "user_type": client.user_type.value
        })

        # 5) Retornar os dados do cliente com os cupons e o JWT
        return {
            # "name": client.name,
            # "email": client.email,
            # "cpf": client.cpf,
            # "coupons": [
            #     {
            #         "hash": coupon.hash,
            #         "discount_percentage": coupon.discount_percentage,
            #         "max_discount": coupon.max_discount,
            #         "expires_at": coupon.expires_at,
            #         "descricao": coupon.descricao,
            #         "vip": coupon.vip
            #     }
            #     for coupon in coupons
            # ],
            "jwt": jwt_token
        }
