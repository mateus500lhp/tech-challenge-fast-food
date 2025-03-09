from app.core.entities.client import Client
from app.core.ports.client_repository_port import ClientRepositoryPort
from app.core.schemas.client_schemas import ClientUpdateIn
from app.shared.validates.cpf_validate import is_cpf_valid

class UpdateClientService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository
        self.allowed_updates = {"cpf", "name", "email", "active", "password"}

    def normalize_and_validate_cpf(self, cpf: str) -> str:
        """
        Remove caracteres não numéricos e valida o CPF.
        """
        digits = "".join(c for c in cpf if c.isdigit())
        if not is_cpf_valid(digits):
            raise ValueError("CPF inválido.")
        return digits

    def validate_updates(self, updates: dict):
        """
        Valida que apenas os campos permitidos estão no payload.
        """
        invalid_keys = set(updates.keys()) - self.allowed_updates
        if invalid_keys:
            raise ValueError(f"Campos inválidos no payload: {', '.join(invalid_keys)}")

    def update_field(self, client: Client, field: str, value):
        """
        Atualiza um campo do cliente, aplicando validações específicas para CPF e e-mail.
        """
        if field == "cpf":
            new_cpf = self.normalize_and_validate_cpf(value)
            existing_cpf = self.client_repository.find_by_cpf(new_cpf)
            if existing_cpf and new_cpf != client.cpf:
                raise ValueError("CPF já cadastrado no sistema.")
            client.cpf = new_cpf

        elif field == "email":
            existing_email = self.client_repository.find_by_email(value)
            if existing_email and value != client.email:
                raise ValueError("Email já cadastrado no sistema.")
            client.email = value

        else:
            setattr(client, field, value)

    def execute(self, cpf: str, updates: dict | ClientUpdateIn) -> Client:
        """
        Atualiza os dados de um cliente após validações.
        :param cpf: CPF do cliente a ser atualizado.
        :param updates: Dados a serem atualizados (dicionário ou `ClientUpdateIn`).
        :return: Cliente atualizado.
        """

        # ✅ Se `updates` for um dicionário, converte para `ClientUpdateIn`
        if isinstance(updates, dict):
            updates = ClientUpdateIn(**updates)

        updates_dict = updates.dict(exclude_unset=True)
        self.validate_updates(updates_dict)

        # 1) Buscar cliente existente pelo CPF
        clean_cpf = self.normalize_and_validate_cpf(cpf)
        existing_client = self.client_repository.find_by_cpf(clean_cpf)
        if not existing_client:
            raise ValueError("Cliente não encontrado.")

        # 2) Iterar sobre os campos e aplicar as alterações
        for field, value in updates_dict.items():
            self.update_field(existing_client, field, value)

        # 3) Salvar alterações no repositório
        return self.client_repository.update(existing_client)
