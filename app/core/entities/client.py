from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.shared.enums.user_type import UserType
from app.shared.validates.cpf_validate import is_cpf_valid


@dataclass
class Client:
    id: Optional[int]
    name: str
    email: str
    cpf: str
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_type: UserType = UserType.CLIENT
    active: bool = True

    def __post_init__(self):
        # Normaliza o CPF removendo caracteres não numéricos
        clean_cpf = "".join(c for c in self.cpf if c.isdigit())
        # Valida o CPF; se inválido, lança uma exceção
        if not is_cpf_valid(clean_cpf):
            raise ValueError("CPF inválido.")
        self.cpf = clean_cpf

