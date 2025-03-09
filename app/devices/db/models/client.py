from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.devices.db.models.base_user import BaseUserModel
from app.shared.enums.user_type import UserType


class ClientModel(BaseUserModel):
    __tablename__ = "clients"
    __mapper_args__ = {
        "polymorphic_identity": UserType.CLIENT,
    }

    id = Column(Integer, ForeignKey("base_users.id"), primary_key=True)


    # Relações com cupons
    coupons_association = relationship("ClientCouponAssociationModel", back_populates="client")
    coupons = relationship("CouponModel", secondary="client_coupons", back_populates="clients")

    # Relação 1:N com OrderModel
    orders = relationship("OrderModel", back_populates="client")

    def __repr__(self):
        return f"<Client(name={self.name}, email={self.email}, cpf={self.cpf})>"
