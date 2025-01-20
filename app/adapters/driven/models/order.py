from sqlalchemy import Column, Integer, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship

from app.adapters.driven.models.base_model import BaseModel
from app.shared.enums.order_status import OrderStatus
from database import Base
class OrderModel(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.RECEIVED)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    amount = Column(Float, nullable=False)

    client = relationship("ClientModel", back_populates="orders")
    items = relationship("OrderItemModel", back_populates="order")
    payment = relationship("PaymentModel", back_populates="order", uselist=False)
    coupon = relationship("CouponModel")

    def __repr__(self):
        return f"<OrderModel(customer_id={self.client_id}, status={self.status}, coupon={self.coupon})>"