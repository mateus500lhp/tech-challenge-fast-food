from database import Base
class CouponModel(Base):
    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True,index=True)
    hash = Column(String,unique=True)
    discount_percentage = Column(Float)
    max_discount = Column(Float)