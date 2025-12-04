import dodopayments
from typing import Dict, Any, Optional
from decimal import Decimal
from uuid import UUID

from src.shared.config.cfg import settings


class DodoPaymentsService:
    """Service for integrating with DodoPayments using official SDK"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'DODO_PAYMENTS_API_KEY', '')
        self.webhook_secret = getattr(settings, 'DODO_PAYMENTS_WEBHOOK_SECRET', '')
        
        # Initialize DodoPayments client
        self.client = dodopayments.DodoPayments(api_key=self.api_key)
    
    async def create_payment_intent(
        self,
        amount: Decimal,
        order_id: UUID,
        customer_email: str,
        customer_name: str,
        currency: str = 'USD',
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a payment intent with DodoPayments"""
        
        payment_data = {
            'amount': int(amount * 100),  # Convert to cents
            'currency': currency,
            'customer_email': customer_email,
            'customer_name': customer_name,
            'metadata': {
                'order_id': str(order_id),
                **(metadata or {})
            },
            'success_url': f"{settings.FRONTEND_URL}/checkout/success?order_id={order_id}",
            'cancel_url': f"{settings.FRONTEND_URL}/checkout/cancel?order_id={order_id}",
            'webhook_url': f"{settings.BACKEND_URL}/api/webhooks/dodo-payments"
        }
        
        return self.client.payments.create(**payment_data)
    
    async def get_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Get payment intent details"""
        return self.client.payments.retrieve(payment_intent_id)
    
    async def confirm_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Confirm a payment intent"""
        return self.client.payments.confirm(payment_intent_id)
    
    async def refund_payment(
        self,
        payment_intent_id: str,
        amount: Optional[Decimal] = None,
        reason: str = "requested_by_customer"
    ) -> Dict[str, Any]:
        """Refund a payment"""
        
        refund_data = {'reason': reason}
        
        if amount:
            refund_data['amount'] = int(amount * 100)  # Convert to cents
        
        return self.client.payments.refund(payment_intent_id, **refund_data)
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature from DodoPayments"""
        try:
            # Try using SDK's webhook verification if available
            return self.client.webhooks.verify_signature(payload, signature, self.webhook_secret)
        except AttributeError:
            # Fallback to manual verification if SDK doesn't provide this method
            import hmac
            import hashlib
            
            expected_signature = hmac.new(
                self.webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    async def create_customer(self, email: str, name: str, user_id: int) -> Dict[str, Any]:
        """Create a customer in DodoPayments"""
        
        customer_data = {
            'email': email,
            'name': name,
            'metadata': {
                'user_id': str(user_id)
            }
        }
        
        return self.client.customers.create(**customer_data)
    
    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details"""
        return self.client.customers.retrieve(customer_id)
