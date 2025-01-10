# main.py
from typing import Annotated, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import SessionLocal

app = FastAPI()


# Exemplo de "schemas" (Pydantic) diretamente no main
# (mas o ideal é movê-los para schemas.py, futuramente)
class UserBase(BaseModel):
    name: str

class ProductBase(BaseModel):
    name: str
    description: str
    price: float


# Dependência para obter sessão de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# -----------------------------------------------------------------------------
# ENDPOINTS
# -----------------------------------------------------------------------------

@app.get("/products", response_model=List[ProductBase])
async def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/products/{product_id}", response_model=ProductBase)
async def get_product_by_id(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=ProductBase)
async def create_new_product(product: ProductBase, db: db_dependency):
    db_product = models.Product(
        name=product.name, 
        description=product.description, 
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
