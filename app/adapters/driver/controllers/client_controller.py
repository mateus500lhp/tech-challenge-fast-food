from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from pydantic import EmailStr

from app.adapters.driver.controllers.client_schemas import (
    ClientIn,
    ClientOut
)
from app.adapters.driven.repositories.client import ClientRepository
from app.domain.entities.client import Client
from app.domain.services.clients.create_client_service import CreateClientService
from app.domain.services.clients.list_client_service import ListClientsService
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

    # Monta a entidade de domínio
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

@router.get("/clients", response_model=List[ClientOut])
def list_clients(db: Session = Depends(get_db_session)):
    repository = ClientRepository(db)
    service = ListClientsService(repository)

    clients = service.execute()

    return [
        ClientOut(
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

@router.get("/clients/cpf/{cpf}", response_model=ClientOut)
def get_client_by_cpf(cpf: str, db: Session = Depends(get_db_session)):
    """
    Busca um cliente pelo CPF.
    """
    repository = ClientRepository(db)
    client_entity = repository.find_by_cpf(cpf)
    if not client_entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found by CPF"
        )
    return ClientOut(
        id=client_entity.id,
        name=client_entity.name,
        email=client_entity.email,
        cpf=client_entity.cpf,
        active=client_entity.active
    )

@router.put("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, client_in: ClientIn, db: Session = Depends(get_db_session)):
    """
    Atualiza os dados de um cliente.
    """
    repository = ClientRepository(db)

    # Verifica se existe
    existing = repository.find_by_id(client_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    # Atualiza os campos
    updated_entity = Client(
        id=client_id,
        name=client_in.name,
        email=client_in.email,
        cpf=client_in.cpf,
        password=client_in.password,
        active=existing.active  # mantém o active existente
    )

    updated_client = repository.update(updated_entity)

    return ClientOut(
        id=updated_client.id,
        name=updated_client.name,
        email=updated_client.email,
        cpf=updated_client.cpf,
        active=updated_client.active
    )

@router.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db_session)):
    """
    Exclui fisicamente um cliente pelo ID.
    """
    repository = ClientRepository(db)
    existing = repository.find_by_id(client_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    repository.delete(client_id)
    return None
