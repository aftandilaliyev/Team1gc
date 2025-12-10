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
    user_id: Optional[str] = None  # Changed to string to match actual webhook
    order_id: Optional[str] = None


class WebhookData(BaseModel):
    subscription_id: Optional[str] = None
    status: str
    product_id: Optional[str] = None
    customer: Optional[Customer] = None
    metadata: Optional[dict] = None  # Changed to dict to handle flexible metadata
    next_billing_date: Optional[datetime] = None
    billing_address: Optional[Address] = None
    shipping_address: Optional[Address] = None
    billing: Optional[dict] = None  # Add billing field from actual webhook
    payment_intent_id: Optional[str] = None
    payment_id: Optional[str] = None  # Add payment_id from actual webhook
    amount: Optional[int] = None
    total_amount: Optional[int] = None  # Add total_amount from actual webhook
    currency: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from webhook


class WebhookRequest(BaseModel):
    data: WebhookData
    type: str  # DodoPayments uses 'type' not 'event_type'
    business_id: Optional[str] = None
    timestamp: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields
