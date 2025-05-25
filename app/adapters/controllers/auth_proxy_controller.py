from fastapi import APIRouter, HTTPException, status

from app.adapters.presenters.client.client_identify_presenter import ClientIdentifyPresenter
from app.core.schemas.client_schemas import ClientIdentifyOut
from app.core.usecases.clients.auth_proxy_service import AuthProxyService

router = APIRouter()

@router.get("/clients/auth/{cpf}", response_model=ClientIdentifyOut)
async def get_client_cognito(cpf: str):
    service = AuthProxyService()
    try:
        jwt_token = await service.execute(cpf)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    return ClientIdentifyPresenter.present(jwt_token)
