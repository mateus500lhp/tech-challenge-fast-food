from typing import Optional

from app.adapters.gateways.client import ClientRepository
from app.core.entities.client import Client
from app.devices.db.connection import get_db_session
from app.shared.handles.jwt_user import verify_jwt
from fastapi.security import HTTPBearer


from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session


security = HTTPBearer()


def get_current_user(
    token: Optional[str]  = Header(None),
    db: Session = Depends(get_db_session),
) -> dict:
    """
    1) Decodifica o JWT e extrai cpf, email e name.
    2) Usa o ClientRepository para buscar por CPF.
    3) Se não existir, instancia seu dataclass Client e chama repo.create().
    4) Retorna sempre a entidade Client.
    """
    try:
        payload = verify_jwt(token)
    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(e))

    cpf   = payload.get("cpf")
    email = payload.get("email", "")
    name  = payload.get("name", "")

    if not cpf:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Token não contém CPF")

    repo = ClientRepository(db)

    client = repo.find_by_cpf(cpf)

    if not client:
        client = Client(
            id=None,
            name=name,
            email=email,
            cpf=cpf,
            created_at=None,
            updated_at=None,
            active=True
        )
        client = repo.create(client)

    return {"user_id": client.id, "payload": payload}