from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from .service import WebhookService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/dodo-payments")
async def handle_dodo_payment_webhook(
    request: Request,
    x_signature: str = Header(..., alias="webhook-signature"),
    db: Session = Depends(get_db)
):
    """Handle DodoPayments webhook events"""
    
    # Get raw request body for signature verification
    body = await request.body()
    
    service = WebhookService(db)
    result = service.handle_dodo_payment_webhook(body, x_signature)
    
    return result
