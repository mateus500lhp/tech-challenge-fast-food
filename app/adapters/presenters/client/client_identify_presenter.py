from app.core.schemas.client_schemas import ClientIdentifyOut

class ClientIdentifyPresenter:
    @staticmethod
    def present(jwt: str) -> ClientIdentifyOut:
        """
        Retorna um objeto `ClientIdentifyOut` contendo apenas o JWT do cliente.
        """
        return ClientIdentifyOut(jwt=jwt)
