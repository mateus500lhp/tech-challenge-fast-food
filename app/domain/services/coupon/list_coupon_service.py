from datetime import date
from typing import List
from app.domain.entities.client import Client
from app.domain.entities.coupon import Coupon
from app.domain.ports.client_repository_port import ClientRepositoryPort
from app.domain.ports.coupon_repository_port import CouponRepositoryPort


class ListCouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def execute(self) -> List[Coupon]:
        # Busca todos os cupons no repositório, desde que estejam ativos e não expirados
        coupons = self.coupon_repository.find_all()
        today = date.today()
        coupons_list = []
        for coupon in coupons:
            if coupon.active and coupon.expires_at >= today:
                coupons_list.append(coupon)
        return coupons_list
    def executeAll(self) -> List[Coupon]:
        # Busca todos os cupons no repositório
        coupons = self.coupon_repository.find_all()
        return coupons
