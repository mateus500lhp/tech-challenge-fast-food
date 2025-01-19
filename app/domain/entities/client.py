from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Client:
    id: Optional[int]
    name: str
    email: str
    cpf: str
    password: str
    active: bool = True
    created_at: datetime = None
    updated_at: datetime = None