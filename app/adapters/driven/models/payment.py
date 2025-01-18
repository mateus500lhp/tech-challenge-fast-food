from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from app.shared.enums.payment_status import PaymentStatus
from database import Base

class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    qr_code = Column(String, nullable=True)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_date = Column(DateTime, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)

    order = relationship("OrderModel", back_populates="payment")

    def __repr__(self):
        return f"<PaymentModel(qr_code={self.qr_code}, status={self.status}, order_id={self.order_id})>"
