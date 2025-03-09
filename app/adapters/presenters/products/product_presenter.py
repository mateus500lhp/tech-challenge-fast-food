from typing import List
from app.core.entities.product import Product
from app.core.schemas.product_schemas import ProductOut

class ProductPresenter:
    @staticmethod
    def present(product: Product) -> ProductOut:
        """Formata um único produto"""
        return ProductOut(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            quantity_available=product.quantity_available
        )

    @staticmethod
    def present_list(products: List[Product]) -> List[ProductOut]:
        """Formata uma lista de produtos"""
        return [ProductPresenter.present(product) for product in products]
