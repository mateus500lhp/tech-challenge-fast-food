from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ClientIn(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    password: str

class ClientUpdateIn(BaseModel):
    name: Optional[str] = Field(None, description="Nome do cliente")
    email: Optional[EmailStr] = Field(None, description="E-mail do cliente")
    cpf: Optional[str] = Field(None, description="CPF do cliente")
    password: Optional[str] = Field(None, description="Senha do cliente")
    active: Optional[bool] = Field(None, description="Status do cliente (ativo ou inativo)")

class ClientOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    cpf: str
    active: bool
class ClientsOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    cpf: str
    active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
class ClientIdentifyOut(BaseModel):
    # name: str
    # email: str
    # cpf: str = Field(..., description="CPF formatado do cliente")
    jwt: str
    # coupons: List[CouponOut] = []

    class Config:
        orm_mode = True
