from datetime import date
from typing import List
from app.core.entities.coupon import Coupon
from app.core.ports.coupon_repository_port import CouponRepositoryPort

class ListCouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def execute(self) -> List[Coupon]:
        """
        Retorna todos os cupons válidos (ativos e não expirados).
        """
        today = date.today()
        return [
            coupon for coupon in self.coupon_repository.find_all()
            if coupon.active and coupon.expires_at >= today
        ]

    def execute_all(self) -> List[Coupon]:
        """
        Retorna todos os cupons, sem filtro de validade.
        """
        return self.coupon_repository.find_all()
