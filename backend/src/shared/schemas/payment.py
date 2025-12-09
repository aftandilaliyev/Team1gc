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
    user_id: Optional[int] = None
    order_id: Optional[str] = None


class WebhookData(BaseModel):
    subscription_id: Optional[str] = None
    status: str
    product_id: Optional[str] = None
    customer: Customer
    metadata: PaymentMetadata | None = None
    next_billing_date: Optional[datetime] = None
    billing_address: Optional[Address] = None
    shipping_address: Optional[Address] = None
    payment_intent_id: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None


class WebhookRequest(BaseModel):
    data: WebhookData
    event_type: str
