from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.adapters.driven.models.base_model import BaseModel
from database import Base

class OrderItemModel(BaseModel):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float)  # O preço do produto no momento do pedido

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel")

    def __repr__(self):
        return f"<OrderItemModel(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"
