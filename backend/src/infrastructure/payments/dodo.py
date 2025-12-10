from math import prod
import dodopayments
from typing import Dict, Any, Optional, List
from decimal import Decimal

from dodopayments.types import AttachExistingCustomerParam, CheckoutSessionResponse, Customer, NewCustomerParam, TaxCategory, Currency, Product as DodoProduct
from dodopayments.types.payment import ProductCart
from dodopayments.types.price_param import OneTimePrice

from src.shared.models.product import Product
from src.shared.config.cfg import settings


class DodoPaymentsService:
    """Service for integrating with DodoPayments using official SDK"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'DODO_PAYMENTS_API_KEY', '')
        self.webhook_secret = getattr(settings, 'DODO_PAYMENTS_WEBHOOK_SECRET', '')
        
        # Initialize DodoPayments client
        self.client = dodopayments.DodoPayments(bearer_token=self.api_key, environment="test_mode")

    def create_checkout_session(
        self,
        cart_items: List[Dict[str, Any]],
        customer_email: str,
        customer_name: str,
        user_id: int,
        order_id: str,
        existing_customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> CheckoutSessionResponse:
        """Create a checkout session with proper SDK classes"""
        
        # Create product cart items
        product_cart = []
        for item in cart_items:
            if not item.get('dodo_product_id'):
                raise ValueError(f"Product {item['product_id']} not synced with DodoPayments")
            
            # Use proper OneTimeProductCartItemParam structure
            product_cart.append(
                ProductCart(
                    product_id=item['dodo_product_id'],
                    quantity=item['quantity']
                )
            )
        
        # Create customer parameter based on whether customer exists
        if existing_customer_id:
            # Use AttachExistingCustomerParam
            customer_param = AttachExistingCustomerParam(customer_id=existing_customer_id)
        else:
            # Use NewCustomerParam
            customer_param = NewCustomerParam(
                email=customer_email,
                name=customer_name,
                metadata={
                    'user_id': str(user_id)
                }
            )

        # Prepare metadata
        final_metadata = {
            'order_id': str(order_id),
            'user_id': str(user_id),
            **(metadata or {})
        }
        
        try:
            return self.client.checkout_sessions.create(
                customer=customer_param,
                product_cart=product_cart,
                metadata=final_metadata,
                return_url=f"{settings.FRONTEND_URL}/checkout/success?order_id={order_id}",
            )
        except Exception:
            # Fallback to simpler structure if the above fails
            return self.client.payments.create(
                customer_email=customer_email,
                customer_name=customer_name,
                product_cart=product_cart,
                metadata=final_metadata,
                return_url=f"{settings.FRONTEND_URL}/checkout/success?order_id={order_id}",
                collect_billing_address=True,
                collect_shipping_address=True
            )
    
    def get_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Get payment intent details"""
        return self.client.payments.retrieve(payment_intent_id)
    
    def confirm_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Confirm a payment intent"""
        return self.client.payments.confirm(payment_intent_id)
    
    def refund_payment(
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
    
    def create_customer(self, email: str, name: str, user_id: int) -> Customer:
        """Create a customer in DodoPayments"""
        
        customer_data = {
            'email': email,
            'name': name,
            'metadata': {
                'user_id': str(user_id)
            }
        }
        
        return self.client.customers.create(**customer_data)
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details"""
        return self.client.customers.retrieve(customer_id)
    
    def create_product_in_dodo(
        self,
        name: str,
        price: Decimal,
        description: str = "",
        metadata: Optional[Dict[str, str]] = None
    ):
        """Create a product in DodoPayments"""
        # Create proper price object for DodoPayments
        price_obj = OneTimePrice(
            price=int(price * 100),  # Convert to cents
            discount=0,
            currency="USD",
            pay_what_you_want=False,
            type="one_time_price",
            purchasing_power_parity=False,
            tax_inclusive=False
        )
        
        return self.client.products.create(
            name=name,
            price=price_obj,
            tax_category="digital_products",
            description=description,
            metadata=metadata or {}
        )
    
    def sync_product_with_dodo(
        self,
        product: Product
    ) -> str:
        """Sync a product with DodoPayments and return the dodo_product_id"""
        
        metadata = {
            'local_product_id': product.id
        }

        dodo_product: DodoProduct = self.create_product_in_dodo(
            name=product.name,
            price=product.price,  # create_product_in_dodo handles cents conversion
            description=product.description,
            metadata=metadata
        )

        return dodo_product.product_id
