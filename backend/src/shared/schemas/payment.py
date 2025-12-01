from datetime import datetime
from pydantic import BaseModel


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str


class PaymentMetadata(BaseModel):
    company_id: str
    user_id: str


class WebhookData(BaseModel):
    subscription_id: str
    status: str
    product_id: str
    customer: Customer
    metadata: PaymentMetadata | None = None
    next_billing_date: datetime


class WebhookRequest(BaseModel):
    data: WebhookData
    event_type: str
