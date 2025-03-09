from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.shared.enums.user_type import UserType


@dataclass
class Client:
    id: Optional[int]
    name: str
    email: str
    cpf: str
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_type: UserType = UserType.CLIENT
    active: bool = True

