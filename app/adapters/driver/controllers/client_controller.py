from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.adapters.driver.controllers.client_schemas import (
    ClientIn,
    ClientOut, ClientIdentifyOut, ClientUpdateIn, ClientsOut
)
from app.adapters.driven.repositories.client import ClientRepository
from app.domain.entities.client import Client
from app.domain.services.clients.create_client_service import CreateClientService
from app.domain.services.clients.identify_client_service import IdentifyClientService
from app.domain.services.clients.list_client_service import ListClientsService
from app.domain.services.clients.update_client_service import UpdateClientService
from database import get_db_session

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
    service = CreateClientService(ClientRepository(db))
    """
        Cria um cliente no sistema
        """
    client = Client(
        id=None,
        name=client_in.name,
        email=client_in.email,
        cpf=client_in.cpf,
        password=client_in.password,
        active=True
    )

    try:
        created = service.execute(client)
        return ClientOut(
            id=created.id,
            name=created.name,
            email=created.email,
            cpf=created.cpf,
            active=created.active
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clients", response_model=List[ClientsOut])
def list_clients(db: Session = Depends(get_db_session)):
    """
        Lista todos os clientes cadastrados no sistema
    """
    repository = ClientRepository(db)
    service = ListClientsService(repository)

    clients = service.execute()

    return [
        ClientsOut(
            id=client.id,
            name=client.name,
            email=client.email,
            cpf=client.cpf,
            active=client.active,
            created_at=client.created_at,
            updated_at=client.updated_at,
        )
        for client in clients
    ]

@router.post(
    "/clients/cpf/{cpf}",
    response_model=ClientIdentifyOut,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "CPF não encontrado no sistema."
                    }
                }
            },
        },
    },
)
def get_client_by_cpf(cpf: str, db: Session = Depends(get_db_session)):
    """
    Busca um cliente pelo CPF, incluindo seus cupons ativos e não expirados.
    """
    repository = ClientRepository(db)
    service = IdentifyClientService(repository)

    try:
        client_with_coupons = service.execute(cpf)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return client_with_coupons
@router.put("/clients/{cpf}", response_model=ClientOut)
def update_client(cpf: str, client_in: ClientUpdateIn, db: Session = Depends(get_db_session)):
    """
    Atualiza os dados de um cliente.
    """
    repository = ClientRepository(db)
    service = UpdateClientService(repository)

    try:
        updates = {key: value for key, value in client_in.dict(exclude_unset=True).items()}
        updated_client = service.execute(cpf=cpf, updates=updates)

        return ClientOut(
            id=updated_client.id,
            name=updated_client.name,
            email=updated_client.email,
            cpf=updated_client.cpf,
            active=updated_client.active
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

@router.delete("/clients/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(cpf: str, db: Session = Depends(get_db_session)):
    """
    Desativar o cliente pelo CPF.
    """
    repository = ClientRepository(db)
    service = UpdateClientService(repository)

    try:
        updates = {"active": False}
        _ = service.execute(cpf=cpf, updates=updates)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

# @router.delete("/clients/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_client(client_id: int, db: Session = Depends(get_db_session)):
#     """
#     Desativar o cliente pelo CPF.
#     """
#     repository = ClientRepository(db)
#     existing = repository.find_by_id(client_id)
#     if not existing:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Client not found"
#         )
#
#     repository.delete(client_id)
#     return None