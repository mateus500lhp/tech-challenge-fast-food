from datetime import date
from app.domain.entities.coupon import Coupon
from app.domain.ports.coupon_repository_port import CouponRepositoryPort


class UpdateCouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def validate_expires_at(self, expires_at: date) -> None:
        """
        Valida se a data de expiração é válida e maior ou igual à data atual.
        """
        today = date.today()
        if expires_at < today:
            raise ValueError("A data de expiração deve ser maior ou igual à data atual.")

    def execute(self, hash: str, updates: dict) -> Coupon:
        """
        Atualiza um cupom existente após realizar validações.

        :param hash: hash do cupom a ser atualizado.
        :param updates: Dicionário contendo os campos a serem atualizados.
        :return: Entidade `Coupon` atualizada.
        """
        # Buscar o cupom existente
        existing_coupon = self.coupon_repository.find_by_hash(hash)
        if not existing_coupon:
            raise ValueError("Cupom não encontrado.")

        # Validar e aplicar atualizações
        if "hash" in updates:
            if " " in updates["hash"]:
                raise ValueError("O hash não pode conter espaços.")
            if len(updates["hash"]) > 20:
                raise ValueError("O hash deve ter no máximo 20 caracteres.")
            hash_conflict = self.coupon_repository.find_by_hash(updates["hash"])
            if hash_conflict and hash_conflict.id != existing_coupon.id:
                raise ValueError("Já existe outro cupom com esse hash.")

        if "discount_percentage" in updates:
            if updates["discount_percentage"] <= 0 or updates["discount_percentage"] > 100:
                raise ValueError("A porcentagem de desconto deve estar entre 0 e 100.")

        if "max_discount" in updates:
            if updates["max_discount"] < 0:
                raise ValueError("O desconto máximo não pode ser negativo.")

        if "expires_at" in updates:
            self.validate_expires_at(updates["expires_at"])

        # Atualizar os campos no cupom existente
        for key, value in updates.items():
            setattr(existing_coupon, key, value)

        # Salvar as alterações no repositório
        updated_coupon = self.coupon_repository.update(existing_coupon)

        return updated_coupon
