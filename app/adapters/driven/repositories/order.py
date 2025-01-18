from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.shared.enums.order_status import OrderStatus
from database import Base
class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.RECEIVED)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)

    cliente = relationship("ClienteModel", back_populates="orders")
    items = relationship("OrderItemModel", back_populates="order")
    coupon = relationship("CouponModel")

    def __repr__(self):
        return f"<OrderModel(customer_id={self.cliente_id}, status={self.status}, coupon={self.coupon})>"