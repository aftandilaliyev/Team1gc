from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.shared.schemas.payment import WebhookRequest
from .service import WebhookService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/dodo-payments")
async def handle_dodo_payment_webhook(
    request: Request,
    webhook_data: WebhookRequest,
    x_signature: str = Header(..., alias="X-Signature"),
    db: Session = Depends(get_db)
):
    """Handle DodoPayments webhook events"""
    
    # Get raw request body for signature verification
    body = await request.body()
    
    service = WebhookService(db)
    result = await service.handle_dodo_payment_webhook(body, x_signature, webhook_data)
    
    return result
