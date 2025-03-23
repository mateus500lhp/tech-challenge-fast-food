from datetime import date
from app.core.entities.coupon import Coupon
from app.core.ports.coupon_repository_port import CouponRepositoryPort

class UpdateCouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def validate_updates(self, existing_coupon: Coupon, updates: dict):
        """Valida todos os campos que serão atualizados."""
        if "hash" in updates:
            self.validate_hash(updates["hash"], existing_coupon)

        if "discount_percentage" in updates or "max_discount" in updates:
            discount_percentage = updates.get("discount_percentage", existing_coupon.discount_percentage)
            max_discount = updates.get("max_discount", existing_coupon.max_discount)
            self.validate_discount(discount_percentage, max_discount)

        if "expires_at" in updates:
            self.validate_expires_at(updates["expires_at"])

    def validate_hash(self, new_hash: str, existing_coupon: Coupon):
        """Valida se o hash é válido e único."""
        if " " in new_hash or len(new_hash) > 20:
            raise ValueError("O hash deve ter no máximo 20 caracteres e não conter espaços.")

        existing = self.coupon_repository.find_by_hash(new_hash)
        if existing and existing.id != existing_coupon.id:
            raise ValueError("Já existe outro cupom com esse hash.")

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

    def execute(self, hash: str, updates: dict) -> Coupon:
        """
        Atualiza um cupom existente.
        """
        existing_coupon = self.coupon_repository.find_by_hash(hash)
        if not existing_coupon:
            raise ValueError("Cupom não encontrado.")

        # Validar os updates antes de aplicá-los
        self.validate_updates(existing_coupon, updates)

        # Aplicar as atualizações ao cupom existente
        for key, value in updates.items():
            setattr(existing_coupon, key, value)

        return self.coupon_repository.update(existing_coupon)
