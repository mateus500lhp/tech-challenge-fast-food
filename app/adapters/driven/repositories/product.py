from sqlalchemy import Column, Integer, String, Float, Enum
from app.shared.enums.categorys import CategoryEnum
from database import Base
class ProductModel(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    quantity_available = Column(Integer, default=0)
    def __repr__(self):
        return f"<ProductModel(name={self.name}, description={self.description}, price={self.price}, category={self.category})>"
