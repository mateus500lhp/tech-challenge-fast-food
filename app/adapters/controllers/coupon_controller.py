from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.adapters.gateways.coupon import CouponRepository
from app.adapters.presenters.coupon.coupon_presenter import CouponPresenter
from app.core.entities.coupon import Coupon
from app.core.usecases.coupon.create_coupon_service import CreateCouponService
from app.core.usecases.coupon.list_coupon_service import ListCouponService
from app.core.schemas.coupon_schemas import CouponIn, CouponOut, CouponUpdateIn
from app.core.usecases.coupon.update_coupon import UpdateCouponService

from app.devices.db.connection import get_db_session

router = APIRouter()

@router.post("/coupons", response_model=CouponOut, status_code=status.HTTP_201_CREATED)
def create_coupon(coupon_in: CouponIn, db: Session = Depends(get_db_session)):
    service = CreateCouponService(CouponRepository(db))
    try:
        coupon = service.execute(coupon_in)
        return CouponPresenter.present(coupon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/coupons", response_model=List[CouponOut])
def list_coupons_valid(db: Session = Depends(get_db_session)):
    service = ListCouponService(CouponRepository(db))
    try:
        return CouponPresenter.present_list(service.execute())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all_coupons", response_model=List[CouponOut])
def list_coupons_all(db: Session = Depends(get_db_session)):
    service = ListCouponService(CouponRepository(db))
    try:
        return CouponPresenter.present_list(service.execute_all())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/coupons/{coupon_hash}", response_model=CouponOut)
def update_coupon(coupon_hash: str, coupon_in: CouponUpdateIn, db: Session = Depends(get_db_session)):
    service = UpdateCouponService(CouponRepository(db))
    try:
        updates = coupon_in.dict(exclude_unset=True)
        return CouponPresenter.present(service.execute(coupon_hash, updates))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/coupons/{coupon_hash}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(coupon_hash: str, db: Session = Depends(get_db_session)):
    service = UpdateCouponService(CouponRepository(db))
    try:
        service.execute(coupon_hash, {"active": False})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
