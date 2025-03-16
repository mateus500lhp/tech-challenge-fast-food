from app.core.entities.payment import Payment
from app.core.schemas.payment_schemas import PaymentStatusResponse

class PaymentPresenter:
    @staticmethod
    def present(payment: Payment) -> PaymentStatusResponse:
        return PaymentStatusResponse(
            order_id=payment.order_id,
            payment_status=payment.status,
            qr_code=payment.qr_code,
        )
