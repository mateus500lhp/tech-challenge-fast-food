from pydantic import EmailStr

from app.core.entities.client import Client
from app.core.ports.client_repository_port import ClientRepositoryPort
from app.core.schemas.client_schemas import ClientIn
from app.shared.validates.cpf_validate import is_cpf_valid

class CreateClientService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository

    # @staticmethod
    # def normalize_and_validate_cpf(cpf: str) -> str:
    #     """
    #     Remove caracteres não numéricos do CPF e valida o formato.
    #     """
    #     clean_cpf = "".join(c for c in cpf if c.isdigit())
    #     if not is_cpf_valid(clean_cpf):
    #         raise ValueError("CPF inválido.")
    #     return clean_cpf

    def validate_unique_fields(self, cpf: str, email: EmailStr):
        """
        Verifica se CPF e e-mail já estão cadastrados no banco.
        """
        if self.client_repository.find_by_cpf(cpf):
            raise ValueError("CPF já cadastrado no sistema.")

        if self.client_repository.find_by_email(email):
            raise ValueError("Email já cadastrado no sistema.")

    def execute(self, client_data: ClientIn) -> Client:
        """
        Valida CPF, verifica duplicidade, formata e cria o cliente no repositório.
        Se ocorrer qualquer problema, lança ValueError com a mensagem adequada.
        """

        client = Client(
            id=None,
            name=client_data.name,
            email=client_data.email,
            cpf=client_data.cpf,  # CPF sem formatação
            password=client_data.password,
            active=True
        )

        self.validate_unique_fields(client.cpf, client_data.email)
        return self.client_repository.create(client)
