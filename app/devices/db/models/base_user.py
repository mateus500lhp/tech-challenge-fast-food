from sqlalchemy import Column, Integer, String, Enum

from app.devices.db.models.base_model import BaseModel
from app.shared.enums.user_type import UserType

class BaseUserModel(BaseModel):
    __tablename__ = "base_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    __mapper_args__ = {
        "polymorphic_on": user_type,
        "polymorphic_identity":  UserType.ADMIN
    }

    @property
    def formatted_cpf(self) -> str:
        """Retorna o CPF com máscara, ex: 123.456.789-01"""
        if not self.cpf or len(self.cpf) != 11:
            return self.cpf or ""
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

    def __repr__(self):
        return f"<BaseUser(name={self.name}, email={self.email}, cpf={self.cpf}, user_type={self.user_type})>"
