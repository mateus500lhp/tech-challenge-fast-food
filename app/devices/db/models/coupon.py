from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.orm import relationship

from app.devices.db.models.base_model import BaseModel


class CouponModel(BaseModel):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True)
    descricao = Column(String)
    discount_percentage = Column(Float,default=0)
    max_discount = Column(Float,default=0)
    expires_at = Column(Date, nullable=True)
    vip = Column(Boolean, nullable=True,default=False)
    clients_association = relationship("ClientCouponAssociationModel", back_populates="coupon", overlaps="clients")
    clients = relationship("ClientModel", secondary="client_coupons", back_populates="coupons", overlaps="clients_association")

    def __repr__(self):
        return f"<CouponModel(code={self.hash}, discount_percentage={self.discount_percentage})>"
