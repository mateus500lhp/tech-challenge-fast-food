from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.adapters.gateways.client import ClientRepository
from app.adapters.presenters.client.client_identify_presenter import ClientIdentifyPresenter
from app.adapters.presenters.client.client_presenter import ClientPresenter
from app.adapters.presenters.client.clients_presenter import ClientsPresenter
from app.core.schemas.client_schemas import ClientOut, ClientIn, ClientsOut, ClientIdentifyOut, ClientUpdateIn
from app.core.usecases.clients.create_client_service import CreateClientService
from app.core.usecases.clients.identify_client_service import IdentifyClientService
from app.core.usecases.clients.list_clients_service import ListClientsService
from app.core.usecases.clients.update_client_service import UpdateClientService
from app.devices.db.connection import get_db_session

router = APIRouter()

@router.post(
    "/clients",
    response_model=ClientOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "CPF já cadastrado no sistema."
                    }
                }
            },
        },
    },
)
def create_client(client_in: ClientIn, db: Session = Depends(get_db_session)):
    """
    Cria um cliente no sistema.
    """
    service = CreateClientService(ClientRepository(db))

    try:
        client = service.execute(client_in)
        return ClientPresenter.present(client)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clients", response_model=List[ClientsOut])
def list_clients(db: Session = Depends(get_db_session)):
    """
    Lista todos os clientes cadastrados no sistema.
    """
    service = ListClientsService(ClientRepository(db))
    clients = service.execute()
    return ClientsPresenter.present(clients)

@router.get("/clients/cpf/{cpf}", response_model=ClientIdentifyOut, status_code=status.HTTP_200_OK)
def get_client_by_cpf(cpf: str, db: Session = Depends(get_db_session)):
    """
    Busca um cliente pelo CPF.
    """
    service = IdentifyClientService(ClientRepository(db))
    try:
        jwt = service.execute(cpf)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ClientIdentifyPresenter.present(jwt)


@router.put("/clients/{cpf}", response_model=ClientOut)
def update_client(cpf: str, client_in: ClientUpdateIn, db: Session = Depends(get_db_session)):
    """
    Atualiza os dados de um cliente.
    """
    service = UpdateClientService(ClientRepository(db))

    try:
        updates = {key: value for key, value in client_in.dict(exclude_unset=True).items()}
        updated_client = service.execute(cpf=cpf, updates=updates)
        return ClientPresenter.present(updated_client)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")


@router.delete("/clients/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(cpf: str, db: Session = Depends(get_db_session)):
    """
    Desativa o cliente pelo CPF.
    """
    service = UpdateClientService(ClientRepository(db))

    try:
        service.execute(cpf=cpf, updates={"active": False})  # Apenas passa o dicionário
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

