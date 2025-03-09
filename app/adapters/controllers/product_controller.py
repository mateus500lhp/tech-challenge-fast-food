from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.adapters.gateways.product import ProductRepository
from app.adapters.presenters.products.product_presenter import ProductPresenter
from app.core.schemas.product_schemas import ProductIn, ProductOut
from app.core.usecases.products.create_product_service import CreateProductService
from app.core.usecases.products.delete_product_service import DeleteProductService
from app.core.usecases.products.list_products_service import ListProductsService, ListProductsByCategoryService
from app.core.usecases.products.update_product_service import UpdateProductService
from app.devices.db.connection import get_db_session
from app.shared.enums.categorys import CategoryEnum

router = APIRouter()

@router.get("/products", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db_session)):
    """Lista todos os produtos"""
    service = ListProductsService(ProductRepository(db))
    return ProductPresenter.present_list(service.execute())

@router.get("/products/category/{category}", response_model=List[ProductOut])
def list_products_by_category(category: CategoryEnum, db: Session = Depends(get_db_session)):
    """Lista produtos por categoria"""
    service = ListProductsByCategoryService(ProductRepository(db))
    return ProductPresenter.present_list(service.execute(category.value))

@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(product_in: ProductIn, db: Session = Depends(get_db_session)):
    """Cria um novo produto"""
    service = CreateProductService(ProductRepository(db))

    try:
        product = service.execute(product_in)
        return ProductPresenter.present(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_in: ProductIn, db: Session = Depends(get_db_session)):
    """Atualiza um produto existente"""
    service = UpdateProductService(ProductRepository(db))

    try:
        updated_product = service.execute(product_id, product_in)
        return ProductPresenter.present(updated_product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db_session)):
    """Deleta um produto"""
    service = DeleteProductService(ProductRepository(db))

    try:
        service.execute(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return
