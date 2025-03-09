from app.core.ports.client_repository_port import ClientRepositoryPort
from app.shared.handles.jwt_user import create_access_token
from app.shared.validates.cpf_validate import is_cpf_valid

class IdentifyClientService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository

    @staticmethod
    def normalize_and_validate_cpf(cpf: str) -> str:
        """
        Remove formatações do CPF e valida o formato.
        """
        clean_cpf = "".join(c for c in cpf if c.isdigit())
        if len(clean_cpf) != 11 or not is_cpf_valid(clean_cpf):
            raise ValueError("CPF inválido.")
        return clean_cpf

    def execute(self, cpf: str) -> str:
        """
        Identifica o cliente pelo CPF e retorna um JWT.

        Args:
            cpf (str): CPF do cliente.

        Returns:
            str: JWT gerado para o cliente.
        """
        # 1) Normalizar e validar o CPF
        clean_cpf = self.normalize_and_validate_cpf(cpf)

        # 2) Buscar cliente no repositório
        client = self.client_repository.find_by_cpf(clean_cpf)
        if not client:
            raise ValueError("CPF não encontrado no sistema.")

        if not client.active:
            raise ValueError("CPF inativado no sistema.")

        # 3) Gerar JWT para o cliente e retornar
        return create_access_token({
            "id": client.id,
            "cpf": client.cpf,
            "email": client.email,
            "name": client.name,
            "user_type": client.user_type.value
        })
