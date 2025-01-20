from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.adapters.driver.controllers.coupon.coupon_schemas import (
    CouponIn,
    CouponOut, CouponUpdateIn,
    # AttachCouponRequest,
)
from app.adapters.driven.repositories.coupon import CouponRepository
from app.domain.entities.coupon import Coupon
from app.domain.services.coupon.create_coupon_service import CreateCouponService
from app.domain.services.coupon.list_coupon_service import ListCouponService
from app.domain.services.coupon.update_coupon import UpdateCouponService
# from app.domain.services.coupons.create_coupon_service import CreateCouponService
# from app.domain.services.coupons.attach_coupon_service import AttachCouponToClientsService
from database import get_db_session

router = APIRouter()


@router.post(
    "/coupons",
    response_model=CouponOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro ao criar cupom."
                    }
                }
            },
        },
    },
)
def create_coupon(coupon_in: CouponIn, db: Session = Depends(get_db_session)):
    """
    Cria um novo cupom no sistema.
    """
    repository = CouponRepository(db)
    service = CreateCouponService(repository)

    coupon = Coupon(
        id=None,
        hash=coupon_in.hash,
        discount_percentage=coupon_in.discount_percentage,
        max_discount=coupon_in.max_discount,
        expires_at=coupon_in.expires_at,
        descricao=coupon_in.descricao,
    )

    try:
        created = service.execute(coupon)
        return CouponOut(
            hash=created.hash,
            discount_percentage=created.discount_percentage,
            max_discount=created.max_discount,
            expires_at=created.expires_at,
            descricao=created.descricao,
            active=created.active,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all_coupons", response_model=List[CouponOut])
def list_coupons(db: Session = Depends(get_db_session)):
    """
    Lista todos os cupons cadastrados no sistema.
    """
    repository = CouponRepository(db)
    service = ListCouponService(repository)

    try:
        coupons = service.executeAll()

        return [
            CouponOut(
                id=coupon.id,
                hash=coupon.hash,
                discount_percentage=coupon.discount_percentage,
                max_discount=coupon.max_discount,
                expires_at=coupon.expires_at,
                descricao=coupon.descricao,
                active=coupon.active,
            )
            for coupon in coupons
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/coupons/{coupon_hash}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(coupon_hash: str, db: Session = Depends(get_db_session)):
    """
    Inativa um cupom do sistema pelo hash.
    """
    repository = CouponRepository(db)
    service = UpdateCouponService(repository)
    try:
        _ = service.execute(coupon_hash,{"active":False})
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/coupons", response_model=List[CouponOut])
def list_coupons_valid(db: Session = Depends(get_db_session)):
    """
    Lista todos os cupons válidos (ativos e não expirados) cadastrados no sistema.
    """
    repository = CouponRepository(db)
    service = ListCouponService(repository)

    try:
        coupons = service.execute()

        return [
            CouponOut(
                id=coupon.id,
                hash=coupon.hash,
                discount_percentage=coupon.discount_percentage,
                max_discount=coupon.max_discount,
                expires_at=coupon.expires_at,
                descricao=coupon.descricao,
                active=coupon.active,
            )
            for coupon in coupons
        ]

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/coupons/{coupon_hash}", response_model=CouponOut)
def update_coupon(coupon_hash: str, coupon_in: CouponUpdateIn, db: Session = Depends(get_db_session)):
    """
    Atualiza os dados de um cupom.
    """
    repository = CouponRepository(db)
    service = UpdateCouponService(repository)

    try:
        # Excluir campos não definidos na solicitação
        updates = {key: value for key, value in coupon_in.dict(exclude_unset=True).items()}

        # Executar a atualização do cupom
        updated_coupon = service.execute(hash=coupon_hash, updates=updates)

        # Retornar o cupom atualizado
        return CouponOut(
            id=updated_coupon.id,
            hash=updated_coupon.hash,
            discount_percentage=updated_coupon.discount_percentage,
            max_discount=updated_coupon.max_discount,
            expires_at=updated_coupon.expires_at,
            active=updated_coupon.active,
            descricao=updated_coupon.descricao,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )