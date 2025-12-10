from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Address(BaseModel):
    line1: Optional[str] = None
    line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str


class PaymentMetadata(BaseModel):
    company_id: Optional[str] = None
    user_id: Optional[str] = None
    order_id: Optional[str] = None


class WebhookData(BaseModel):
    customer: Optional[Customer] = None
    metadata: Optional[dict] = None
    billing: Optional[dict] = None
    payment_intent_id: Optional[str] = None
    payment_id: Optional[str] = None
    total_amount: Optional[int] = None
    currency: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from webhook


class WebhookRequest(BaseModel):
    data: WebhookData
    type: str  # DodoPayments uses 'type' not 'event_type'

    class Config:
        extra = "allow"  # Allow extra fields
