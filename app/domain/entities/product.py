from dataclasses import dataclass
from typing import Optional

from app.shared.enums.categorys import CategoryEnum


@dataclass
class Product:
    name: str
    description: str
    price: float
    category: CategoryEnum
    quantity_available: int = 0