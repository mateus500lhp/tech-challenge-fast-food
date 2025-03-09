from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.devices.db.models.base_model import BaseModel


class ClientCouponAssociationModel(BaseModel):
    __tablename__ = "client_coupons"

    client_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), primary_key=True)

    client = relationship("ClientModel", back_populates="coupons_association", overlaps="coupons")
    coupon = relationship("CouponModel", back_populates="clients_association", overlaps="clients")