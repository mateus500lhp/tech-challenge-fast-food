from app.domain.entities.client import Client
from app.domain.ports.client_repository_port import ClientRepositoryPort
from app.shared.validates.cpf_validate import is_cpf_valid


class CreateClientService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository

    def normalize_and_validate_cpf(self,cpf: str) -> str:
        # remove não-dígitos
        digits = "".join(c for c in cpf if c.isdigit())
        return digits

    def execute(self, client: Client) -> Client:
        """
               Valida CPF, verifica duplicidade, formata e cria o cliente no repositório.
               Se ocorrer qualquer problema, lança ValueError com a mensagem adequada.
               """

        # 1) Validar CPF
        if not is_cpf_valid(client.cpf):
            raise ValueError("CPF inválido.")

        # 2) Serializer CPF
        clean_cpf = self.normalize_and_validate_cpf(client.cpf)

        # 3) Verificar se CPF já está cadastrado
        existing = self.client_repository.find_by_cpf(clean_cpf)
        if existing:
            raise ValueError("CPF já cadastrado no sistema.")

        # 4) Verificar se email já está cadastrado
        existing = self.client_repository.find_by_email(client.email)
        if existing:
            raise ValueError("Email já cadastrado no sistema.")

        # 5) Substitui o CPF do objeto em memória para já ficar sem formatação
        client.cpf = clean_cpf

        # 6) Cria no repositório
        created_client = self.client_repository.create(client)
        return created_client
