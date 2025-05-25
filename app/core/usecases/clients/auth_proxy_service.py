from dotenv import load_dotenv

from app.shared.validates.cpf_validate import is_cpf_valid
import os, httpx
from fastapi import HTTPException, status

load_dotenv()

class AuthProxyService:
    def __init__(self, auth_endpoint: str = os.getenv("AUTH_ENDPOINT")):
        self.auth_endpoint = auth_endpoint

    @staticmethod
    def normalize_and_validate_cpf(cpf: str) -> str:
        """
        Remove formatações do CPF e valida o formato.
        """
        clean_cpf = "".join(c for c in cpf if c.isdigit())
        if len(clean_cpf) != 11 or not is_cpf_valid(clean_cpf):
            raise ValueError("CPF inválido.")
        return clean_cpf


    async def execute(self, cpf: str) -> str:
        clean_cpf = self.normalize_and_validate_cpf(cpf)

        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(self.auth_endpoint, json={"cpf": clean_cpf})

        if resp.status_code == 200:
            return resp.json()["token"]

        if resp.status_code == 404:
            print(resp.text)
            raise ValueError("CPF não encontrado no Cognito.")
        if resp.status_code == 400:
            print(resp.text)
            raise ValueError("CPF inválido (Lambda).")

        # Qualquer outro erro → 502 Bad Gateway
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Erro no serviço de autenticação")