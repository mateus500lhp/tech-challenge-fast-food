from sqlalchemy import Column, Integer, String, Float
from database import Base
class CouponModel(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True)
    discount_percentage = Column(Float,default=0)
    max_discount = Column(Float,default=0)

    def __repr__(self):
        return f"<CouponModel(code={self.hash}, discount_percentage={self.discount_percentage})>"
