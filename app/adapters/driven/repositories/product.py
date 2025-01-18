from typing import List, Optional
from sqlalchemy.orm import Session

from app.adapters.driven.models import ProductModel
from app.domain.entities.product import Product
from app.domain.ports.products_repository_port import ProductRepositoryPort


class ProductRepository(ProductRepositoryPort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, product: Product) -> Product:
        product_model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            quantity_available=product.quantity_available
        )
        self.db_session.add(product_model)
        self.db_session.commit()
        self.db_session.refresh(product_model)
        # Converte de volta para a dataclass
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            category=product_model.category,
            quantity_available=product_model.quantity_available
        )

    def find_by_id(self, product_id: int) -> Optional[Product]:
        product_model = self.db_session.query(ProductModel).get(product_id)
        if not product_model:
            return None
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            category=product_model.category,
            quantity_available=product_model.quantity_available
        )

    def find_all(self) -> List[Product]:
        product_models = self.db_session.query(ProductModel).all()
        return [
            Product(
                id=m.id,
                name=m.name,
                description=m.description,
                price=m.price,
                category=m.category,
                quantity_available=m.quantity_available
            )
            for m in product_models
        ]

    def update(self, product: Product) -> Product:
        product_model = self.db_session.query(ProductModel).get(product.id)
        if not product_model:
            raise ValueError("Product not found")
        product_model.name = product.name
        product_model.description = product.description
        product_model.price = product.price
        product_model.category = product.category
        product_model.quantity_available = product.quantity_available
        self.db_session.commit()
        self.db_session.refresh(product_model)
        return Product(
            id=product_model.id,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            category=product_model.category,
            quantity_available=product_model.quantity_available
        )

    def delete(self, product_id: int) -> None:
        product_model = self.db_session.query(ProductModel).get(product_id)
        if product_model:
            self.db_session.delete(product_model)
            self.db_session.commit()
