from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ClientCouponAssociationModel(Base):
    __tablename__ = "client_coupons"

    client_id = Column(Integer, ForeignKey("clients.id"), primary_key=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), primary_key=True)

    client = relationship("ClientModel", back_populates="coupons_association")
    coupon = relationship("CouponModel", back_populates="clients_association")