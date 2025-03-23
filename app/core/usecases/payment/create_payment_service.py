from app.core.entities.order import Order
from app.core.entities.payment import Payment
from app.adapters.gateways.payment import PaymentRepository
from app.core.schemas.payment_schemas import PaymentQRCode
from app.shared.enums.payment_status import PaymentStatus
from app.shared.generate_qr_data import generate_qr_data

class PaymentService:
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def execute(self, order: Order) -> PaymentQRCode:
        """
        Gera os dados do QRCode, cria o pagamento com status PENDING e retorna o QRCode.
        """
        qr_data = generate_qr_data(order.id, order.amount)
        payment = Payment(
            id = None,
            qr_code=qr_data,
            status=PaymentStatus.PENDING,
            order_id=order.id,
            amount=order.amount,
            description="Pagamento pendente"
        )
        self.payment_repository.create(payment)
        return PaymentQRCode(qr_data=qr_data)