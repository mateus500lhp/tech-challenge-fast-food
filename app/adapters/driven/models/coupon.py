from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.adapters.driven.models.base_model import BaseModel

class CouponModel(BaseModel):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True)
    discount_percentage = Column(Float,default=0)
    max_discount = Column(Float,default=0)

    clients_association = relationship("ClientCouponAssociationModel", back_populates="coupon")
    clients = relationship("ClientModel", secondary="client_coupons", back_populates="coupons")

    def __repr__(self):
        return f"<CouponModel(code={self.hash}, discount_percentage={self.discount_percentage})>"
