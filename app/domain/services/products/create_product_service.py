from app.domain.entities.product import Product
from app.domain.ports.products_repository_port import ProductRepositoryPort


class CreateProductService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self, product: Product) -> Product:
        # Exemplo de regra simples: se price < 0, erro.
        if product.price < 0:
            raise ValueError("Price cannot be negative.")
        # Cria no repositório
        return self.product_repository.create(product)
