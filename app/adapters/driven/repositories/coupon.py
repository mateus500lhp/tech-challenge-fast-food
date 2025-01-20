from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session
from app.adapters.driven.models import CouponModel
from app.domain.entities.coupon import Coupon  # Entidade de domínio
from app.domain.ports.coupon_repository_port import CouponRepositoryPort


class CouponRepository(CouponRepositoryPort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, coupon: Coupon) -> Coupon:
        """
        Cria um novo cupom no banco de dados.
        """
        coupon_model = CouponModel(
            hash=coupon.hash,
            discount_percentage=coupon.discount_percentage,
            max_discount=coupon.max_discount,
            expires_at=coupon.expires_at,
            descricao=coupon.descricao,
        )
        self.db_session.add(coupon_model)
        self.db_session.commit()
        self.db_session.refresh(coupon_model)

        return Coupon(
            id=coupon_model.id,
            hash=coupon_model.hash,
            discount_percentage=coupon_model.discount_percentage,
            max_discount=coupon_model.max_discount,
            expires_at=coupon_model.expires_at,
            descricao=coupon_model.descricao,
            active=coupon_model.active,
        )

    def find_by_hash(self, coupon_hash: str) -> Optional[Coupon]:
        """
        Busca um cupom pelo hash único.
        """
        coupon_model = (
            self.db_session.query(CouponModel)
            .filter(CouponModel.hash == coupon_hash)
            .first()
        )
        if not coupon_model:
            return None

        return Coupon(
            id=coupon_model.id,
            hash=coupon_model.hash,
            discount_percentage=coupon_model.discount_percentage,
            max_discount=coupon_model.max_discount,
            expires_at=coupon_model.expires_at,
            descricao=coupon_model.descricao,
            active=coupon_model.active,
        )

    def find_all(self) -> List[Coupon]:
        """
        Retorna todos os cupons cadastrados.
        """
        coupon_models = self.db_session.query(CouponModel).all()
        return [
            Coupon(
                id=c.id,
                hash=c.hash,
                discount_percentage=c.discount_percentage,
                max_discount=c.max_discount,
                expires_at=c.expires_at,
                descricao=c.descricao,
                active=c.active,
            )
            for c in coupon_models
        ]

    def update(self, coupon: Coupon) -> Coupon:
        """
        Atualiza um cupom existente.
        """
        coupon_model = self.db_session.query(CouponModel).get(coupon.id)
        if not coupon_model:
            raise ValueError("Coupon not found")

        coupon_model.hash = coupon.hash
        coupon_model.discount_percentage = coupon.discount_percentage
        coupon_model.max_discount = coupon.max_discount
        coupon_model.expires_at = coupon.expires_at
        coupon_model.active = coupon.active
        coupon_model.descricao = coupon.descricao

        self.db_session.commit()
        self.db_session.refresh(coupon_model)

        return Coupon(
            id=coupon_model.id,
            hash=coupon_model.hash,
            discount_percentage=coupon_model.discount_percentage,
            max_discount=coupon_model.max_discount,
            expires_at=coupon_model.expires_at,
            descricao=coupon_model.descricao,
            active=coupon_model.active,
        )

    def delete(self, coupon_id: int) -> None:
        """
        Remove um cupom pelo ID.
        """
        coupon_model = self.db_session.query(CouponModel).get(coupon_id)
        if coupon_model:
            self.db_session.delete(coupon_model)
            self.db_session.commit()