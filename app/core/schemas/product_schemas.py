# Schemas de entrada/saída para a API
from pydantic import BaseModel
from app.shared.enums.categorys import CategoryEnum


class ProductIn(BaseModel):
    name: str
    description: str | None
    price: float
    category: CategoryEnum
    quantity_available: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    category: CategoryEnum
    quantity_available: int
