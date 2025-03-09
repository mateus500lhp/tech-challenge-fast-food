from datetime import date
from app.core.entities.coupon import Coupon
from app.core.ports.coupon_repository_port import CouponRepositoryPort

class CreateCouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def validate_coupon(self, coupon: Coupon):
        """Valida todas as regras do cupom antes de criar."""
        self.validate_hash(coupon.hash)
        self.validate_discount(coupon.discount_percentage, coupon.max_discount)
        self.validate_expires_at(coupon.expires_at)

        # Verifica se o hash já existe no banco
        if self.coupon_repository.find_by_hash(coupon.hash):
            raise ValueError("Já existe um cupom com esse hash.")

    @staticmethod
    def validate_hash(hash_value: str):
        """Valida o formato do hash."""
        if " " in hash_value:
            raise ValueError("O hash não pode conter espaços.")
        if len(hash_value) > 20:
            raise ValueError("O hash deve ter no máximo 20 caracteres.")

    @staticmethod
    def validate_discount(discount_percentage: float, max_discount: float):
        """Valida os valores de desconto."""
        if not (0 < discount_percentage <= 100):
            raise ValueError("A porcentagem de desconto deve estar entre 0 e 100.")
        if max_discount < 0:
            raise ValueError("O desconto máximo não pode ser negativo.")

    @staticmethod
    def validate_expires_at(expires_at: date):
        """Valida a data de expiração do cupom."""
        if expires_at < date.today():
            raise ValueError("A data de expiração deve ser maior ou igual à data atual.")

    def execute(self, coupon: Coupon) -> Coupon:
        """
        Cria um novo cupom após validações.
        """
        self.validate_coupon(coupon)
        return self.coupon_repository.create(coupon)
