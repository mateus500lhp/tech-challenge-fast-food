from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.adapters.driven.repositories.base_user import BaseUserModel
from app.shared.enums.user_type import UserType

class ClientModel(BaseUserModel):
    __tablename__ = "clients"

    id = Column(Integer, ForeignKey("base_users.id"), primary_key=True)
    user_type = UserType.CLIENT.value
    coupons_association = relationship("ClientCouponAssociationModel", back_populates="client")
    coupons = relationship("CouponModel", secondary="client_coupons", back_populates="clients")

    def __repr__(self):
        return f"<Client(name={self.name}, email={self.email}, cpf={self.cpf})>"
