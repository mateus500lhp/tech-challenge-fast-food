from app.domain.entities.client import Client
from app.domain.ports.client_repository_port import ClientRepositoryPort
from app.shared.validates.cpf_validate import is_cpf_valid

class UpdateClientService:
    def __init__(self, client_repository: ClientRepositoryPort):
        self.client_repository = client_repository
        self.allowed_updates = {"cpf", "name", "email", "active", "password"}

    def normalize_and_validate_cpf(self, cpf: str) -> str:
        """Remove caracteres não numéricos e valida o CPF."""
        digits = "".join(c for c in cpf if c.isdigit())
        if not is_cpf_valid(digits):
            raise ValueError("CPF inválido.")
        return digits

    def validate_updates(self, updates: dict):
        """Valida que apenas os campos permitidos estão no payload."""
        invalid_keys = set(updates.keys()) - self.allowed_updates
        if invalid_keys:
            raise ValueError(f"Campos inválidos no payload: {', '.join(invalid_keys)}")

    def execute(self, cpf: str, updates: dict) -> Client:
        """
        Atualiza os dados de um cliente após validações.
        :param cpf: cpf do cliente a ser atualizado.
        :param updates: Dados a serem atualizados (e.g., name, email, cpf, etc.).
        :return: Cliente atualizado.
        """
        self.validate_updates(updates)

        # 1) Buscar cliente existente pelo cpf
        clean_cpf = self.normalize_and_validate_cpf(cpf)
        existing_client = self.client_repository.find_by_cpf(clean_cpf)
        if not existing_client:
            raise ValueError("Cliente não encontrado.")

        # 2) Atualizar e validar os campos
        if "cpf" in updates:
            clean_cpf_update = self.normalize_and_validate_cpf(updates["cpf"])
            if self.client_repository.find_by_cpf(clean_cpf) and clean_cpf_update != existing_client.cpf:
                raise ValueError("CPF já cadastrado no sistema.")
            existing_client.cpf = clean_cpf_update

        if "email" in updates:
            email = updates["email"]
            if self.client_repository.find_by_email(email) and email != existing_client.email:
                raise ValueError("Email já cadastrado no sistema.")
            existing_client.email = email

        if "name" in updates:
            existing_client.name = updates["name"]

        if "password" in updates:
            existing_client.password = updates["password"]

        if "active" in updates:
            existing_client.active = updates["active"]

        # 3) Salvar alterações no repositório
        updated_client = self.client_repository.update(existing_client)

        return updated_client
