from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientIn(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    password: str

class ClientOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    cpf: str
    active: bool
    created_at: datetime | None
    updated_at: datetime | None
