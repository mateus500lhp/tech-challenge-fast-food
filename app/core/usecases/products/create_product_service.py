from app.core.entities.product import Product
from app.core.ports.products_repository_port import ProductRepositoryPort
from app.core.schemas.product_schemas import ProductIn

class CreateProductService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self, product_data: ProductIn) -> Product:
        """Cria um novo produto após validações"""

        if product_data.price < 0:
            raise ValueError("Price cannot be negative.")

        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category.value,
            quantity_available=product_data.quantity_available
        )

        return self.product_repository.create(product)
