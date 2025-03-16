from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.adapters.presenters.payment.payment_presenter import PaymentPresenter
from app.core.schemas.payment_schemas import PaymentWebhookRequest
from app.core.usecases.payment.update_payment_status_service import UpdatePaymentStatusService
from app.devices.db.connection import get_db_session
from app.adapters.gateways.payment import PaymentRepository

router = APIRouter()

@router.post("/webhooks/payment")
def payment_webhook(payload: PaymentWebhookRequest, db: Session = Depends(get_db_session)):
    """
    Webhook para receber a confirmação de pagamento.
    O payload deve conter o order_id, o novo status de pagamento e opcionalmente uma descrição.
    """
    payment_repo = PaymentRepository(db)
    service = UpdatePaymentStatusService(payment_repo)
    try:
        updated_payment = service.execute(
            payload.order_id, payload.payment_status, payload.description
        )
        return PaymentPresenter.present(updated_payment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
