import uuid
from datetime import datetime, date

from app.domain.entities.coupon import Coupon
from app.domain.ports.coupon_repository_port import CouponRepositoryPort


class CreateCouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def validate_expires_at(self, expires_at: date) -> None:
        """
        Valida se a data de expiração é válida e maior ou igual à data atual.
        """
        today = date.today()
        if expires_at < today:
            raise ValueError("A data de expiração deve ser maior ou igual à data atual.")

    def execute(self, coupon: Coupon) -> Coupon:
        """
        Cria um novo cupom após realizar validações e gerar um hash único.

        :param coupon: Entidade de domínio `Coupon` (sem hash definido inicialmente).
        :return: Entidade `Coupon` criada
        """
        if " " in coupon.hash:
            raise ValueError("Não pode conter espaços no hash")

        # valida hash único para o cupom
        if len(coupon.hash)>20:
            raise ValueError("O hash deve ter no máximo 20 caracteres.")

        coupon_exist = self.coupon_repository.find_by_hash(coupon.hash)
        if coupon_exist:
            raise ValueError("Já existe um cupom com esse hash.")

        # Validações adicionais (exemplo: porcentagem de desconto)
        if coupon.discount_percentage <= 0 or coupon.discount_percentage > 100:
            raise ValueError("A porcentagem de desconto deve estar entre 0 e 100.")

        # Validação para max_discount (não pode ser negativo)
        if coupon.max_discount < 0:
            raise ValueError("O desconto máximo não pode ser negativo.")

        if coupon.expires_at:
            self.validate_expires_at(coupon.expires_at)
        else:
            raise ValueError("A data de expiração (expires_at) é obrigatória.")

        # Criar o cupom no repositório
        created_coupon = self.coupon_repository.create(coupon)

        return created_coupon
