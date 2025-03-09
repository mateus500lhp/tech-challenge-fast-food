from app.core.entities.client import Client
from app.core.schemas.client_schemas import ClientOut

class ClientPresenter:
    @staticmethod
    def present(client: Client) -> ClientOut:
        """
        Converte uma entidade `Client` para um `ClientOut`, formatando o CPF.
        """
        return ClientOut(
            id=client.id,
            name=client.name,
            email=client.email,
            cpf=ClientPresenter.format_cpf(client.cpf),
            active=client.active
        )

    @staticmethod
    def format_cpf(cpf: str) -> str:
        """Aplica máscara no CPF: 123.456.789-00"""
        if not cpf or len(cpf) != 11:
            return cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
