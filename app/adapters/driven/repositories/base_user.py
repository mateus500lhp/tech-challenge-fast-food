from sqlalchemy import Column, Integer, String, Enum
from app.shared.enums.user_type import UserType
from database import Base

class BaseUserModel(Base):
    __tablename__ = "base_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

    def __repr__(self):
        return f"<BaseUser(name={self.name}, email={self.email}, cpf={self.cpf}, user_type={self.user_type})>"
