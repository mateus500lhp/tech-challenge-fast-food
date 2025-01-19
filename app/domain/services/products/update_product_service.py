from app.domain.entities.product import Product
from app.domain.ports.products_repository_port import ProductRepositoryPort

class UpdateProductService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self, product_id: int, new_data: Product) -> Product:
        # Buscar produto existente
        existing_product = self.product_repository.find_by_id(product_id)
        if not existing_product:
            raise ValueError("Product not found")

        # Se tiver alguma lógica/validação extra, colocar aqui
        if new_data.price < 0:
            raise ValueError("Price cannot be negative.")

        # Atualizar campos do objeto existente
        existing_product.name = new_data.name
        existing_product.description = new_data.description
        existing_product.price = new_data.price
        existing_product.category = new_data.category
        existing_product.quantity_available = new_data.quantity_available

        # Chamar repositório para persistir as mudanças
        return self.product_repository.update(existing_product)
