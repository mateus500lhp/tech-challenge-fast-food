from typing import Optional

from sqlalchemy.orm import Session
from app.core.entities.payment import Payment
from app.core.ports.payment_repository_port import PaymentRepositoryPort
from app.devices.db.models import PaymentModel

class PaymentRepository(PaymentRepositoryPort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, payment: Payment) -> Payment:
        payment_model = PaymentModel(
            order_id=payment.order_id,
            qr_code=payment.qr_code,
            status=payment.status,
            payment_date=payment.payment_date,
            description=payment.description,
            amount=payment.amount,
        )
        self.db_session.add(payment_model)
        self.db_session.commit()
        self.db_session.refresh(payment_model)

        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            qr_code=payment_model.qr_code,
            status=payment_model.status,
            payment_date=payment_model.payment_date,
            description=payment_model.description,
            amount=payment_model.amount,
        )

    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        payment_model = (
            self.db_session.query(PaymentModel)
            .filter(PaymentModel.order_id == order_id)
            .first()
        )
        if not payment_model:
            return None

        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            qr_code=payment_model.qr_code,
            status=payment_model.status,
            payment_date=payment_model.payment_date,
            description=payment_model.description,
            amount=payment_model.amount,
        )

    def update(self, payment: Payment) -> Payment:
        payment_model = self.db_session.query(PaymentModel).get(payment.id)
        if not payment_model:
            raise ValueError("Pagamento não encontrado.")
        payment_model.status = payment.status
        payment_model.description = payment.description
        payment_model.payment_date = payment.payment_date
        self.db_session.commit()
        self.db_session.refresh(payment_model)
        return Payment(
            id=payment_model.id,
            order_id=payment_model.order_id,
            qr_code=payment_model.qr_code,
            status=payment_model.status,
            payment_date=payment_model.payment_date,
            description=payment_model.description,
            amount=payment_model.amount,
        )
