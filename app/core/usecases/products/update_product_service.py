from app.core.entities.product import Product
from app.core.ports.products_repository_port import ProductRepositoryPort
from app.core.schemas.product_schemas import ProductIn

class UpdateProductService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self, product_id: int, product_data: ProductIn) -> Product:
        """Atualiza um produto existente"""

        existing_product = self.product_repository.find_by_id(product_id)
        if not existing_product:
            raise ValueError("Product not found")

        if product_data.price < 0:
            raise ValueError("Price cannot be negative.")

        # Atualiza os campos do produto existente
        existing_product.name = product_data.name
        existing_product.description = product_data.description
        existing_product.price = product_data.price
        existing_product.category = product_data.category.value
        existing_product.quantity_available = product_data.quantity_available

        return self.product_repository.update(existing_product)
