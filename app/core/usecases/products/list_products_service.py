from typing import List
from app.core.entities.product import Product
from app.core.ports.products_repository_port import ProductRepositoryPort

class ListProductsService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self) -> List[Product]:
        return self.product_repository.find_all()


class ListProductsByCategoryService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self, category: str) -> List[Product]:
        return self.product_repository.find_by_category(category)
