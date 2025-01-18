from typing import List

from app.domain.entities.product import Product
from app.domain.ports.products_repository_port import ProductRepositoryPort


class ListProductsService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self) -> List[Product]:
        return self.product_repository.find_all()
