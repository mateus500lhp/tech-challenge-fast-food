from app.core.schemas.coupon_schemas import CouponOut
from app.core.entities.coupon import Coupon

class CouponPresenter:
    @staticmethod
    def present(coupon: Coupon) -> CouponOut:
        """
        Retorna um objeto `CouponOut` formatado para resposta da API.
        """
        return CouponOut(
            hash=coupon.hash,
            discount_percentage=coupon.discount_percentage,
            max_discount=coupon.max_discount,
            expires_at=coupon.expires_at,
            descricao=coupon.descricao,
            active=coupon.active,
        )

    @staticmethod
    def present_list(coupons: list[Coupon]) -> list[CouponOut]:
        """
        Retorna uma lista de cupons formatados.
        """
        return [CouponPresenter.present(coupon) for coupon in coupons]
