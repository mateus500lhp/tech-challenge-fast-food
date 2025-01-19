from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from pydantic import BaseModel

from app.adapters.driven.repositories.product import ProductRepository
from app.domain.entities.product import Product
from app.domain.services.products.create_product_service import CreateProductService
from app.domain.services.products.delete_product_service import DeleteProductService
from app.domain.services.products.list_products_service import ListProductsService, ListProductsByCategoryService
from app.domain.services.products.update_product_service import UpdateProductService
from app.shared.enums.categorys import CategoryEnum
from database import get_db_session

router = APIRouter()

# Schemas de entrada/saída para a API
class ProductIn(BaseModel):
    name: str
    description: str | None
    price: float
    category: CategoryEnum
    quantity_available: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    category: CategoryEnum
    quantity_available: int

@router.get("/products", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db_session)):
    repo = ProductRepository(db)
    use_case = ListProductsService(repo)
    products = use_case.execute()
    # Converte para Pydantic (para retornar via JSON)
    return [
        ProductOut(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category.value,  # se for CategoryEnum, .value
            quantity_available=p.quantity_available
        )
        for p in products
    ]

@router.get("/products/category/{category}", response_model=List[ProductOut])
def list_products_by_category(category: CategoryEnum, db: Session = Depends(get_db_session)):
    repo = ProductRepository(db)
    use_case = ListProductsByCategoryService(repo)

    # Chama o serviço de listagem por categoria
    products = use_case.execute(category.value)
    return [
        ProductOut(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category.value,
            quantity_available=p.quantity_available
        )
        for p in products
    ]

@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(product_in: ProductIn, db: Session = Depends(get_db_session)):
    repo = ProductRepository(db)
    use_case = CreateProductService(repo)
    # Converte Pydantic -> Domain
    product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        category=product_in.category.value,
        quantity_available=product_in.quantity_available
    )

    try:
        created = use_case.execute(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ProductOut(
        id=created.id,
        name=created.name,
        description=created.description,
        price=created.price,
        category=created.category.value,  # category é Enum
        quantity_available=created.quantity_available
    )

@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_in: ProductIn, db: Session = Depends(get_db_session)):
    repo = ProductRepository(db)
    use_case = UpdateProductService(repo)

    updated_data = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        category=product_in.category.value,
        quantity_available=product_in.quantity_available
    )

    try:
        updated_product = use_case.execute(product_id, updated_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ProductOut(
        id=updated_product.id,
        name=updated_product.name,
        description=updated_product.description,
        price=updated_product.price,
        category=updated_product.category.value,
        quantity_available=updated_product.quantity_available
    )

@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db_session)):
    repo = ProductRepository(db)
    use_case = DeleteProductService(repo)

    try:
        use_case.execute(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return