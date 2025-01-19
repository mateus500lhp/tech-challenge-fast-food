from app.domain.ports.products_repository_port import ProductRepositoryPort

class DeleteProductService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> None:
        existing_product = self.product_repository.find_by_id(product_id)
        if not existing_product:
            raise ValueError("Product not found")

        # Se houver alguma regra extra, colocar aqui...
        self.product_repository.delete(product_id)
