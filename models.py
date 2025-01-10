from itertools import product

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    tipo = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)