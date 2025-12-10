import json
from typing import Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.shared.models.order import Order, OrderItem, OrderStatus, CartItem
from src.shared.models.user import User
from src.shared.schemas.payment import WebhookRequest
from src.infrastructure.payments import DodoPaymentsService




class WebhookService:
    def __init__(self, session: Session):
        self.session = session
        self.dodo_payments = DodoPaymentsService()

    def handle_dodo_payment_webhook(
        self, 
        payload: bytes, 
        signature: str
    ) -> Dict[str, Any]:
        """Handle DodoPayments webhook events"""
        
        # Verify webhook signature
        #if not self.dodo_payments.verify_webhook_signature(payload, signature):
        #    raise HTTPException(
        #        status_code=status.HTTP_400_BAD_REQUEST,
        #        detail="Invalid webhook signature"
        #    )

        # extract schema from payload
        try:
            # First parse JSON
            json_payload = json.loads(payload)
            print(f"Parsed JSON payload: {json_payload}")  # Debug log
            
            # Then validate with schema
            payload = WebhookRequest(**json_payload)
            print(f"Successfully parsed webhook: {payload.type}")  # Debug log
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # Debug log
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid JSON payload: {str(e)}"
            )
        except Exception as e:
            print(f"Schema validation error: {e}")  # Debug log
            print(f"Raw payload: {payload}")  # Debug log
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid webhook payload: {str(e)}"
            )
        
        event_type = payload.type  # DodoPayments uses 'type' field
        data = payload.data
        
        # Extract user ID from metadata
        user_id = None
        if data.metadata and isinstance(data.metadata, dict):
            user_id_str = data.metadata.get('user_id')
            if user_id_str:
                try:
                    user_id = int(user_id_str)
                except (ValueError, TypeError):
                    pass
        
        if not user_id:
            return {"status": "ignored", "reason": "No user_id in metadata"}
        
        # Check if order_id exists in metadata (for backward compatibility)
        order_id = None
        if data.metadata and isinstance(data.metadata, dict):
            order_id_val = data.metadata.get('order_id')
            if order_id_val and order_id_val != "None":
                order_id = str(order_id_val)
        
        # Get existing order if order_id is provided
        order = None
        if order_id:
            order = self.session.query(Order).filter(Order.id == order_id).first()
        
        # Handle different event types
        if event_type == "payment.succeeded":
            return self._handle_payment_succeeded(order, data, user_id)
        elif event_type == "payment.failed":
            return self._handle_payment_failed(order, data, user_id)
        elif event_type == "payment.refunded":
            return self._handle_payment_refunded(order, data, user_id)
        else:
            # Unknown event type, just log and return success
            return {"status": "ignored", "reason": f"Unknown event type: {event_type}"}

    def _handle_payment_succeeded(self, order: Order, data: Any, user_id: int) -> Dict[str, Any]:
        """Handle successful payment - create order from cart items and clear cart"""
        
        # If order already exists, just update it
        if order:
            if order.status == OrderStatus.PENDING.value:
                order.status = OrderStatus.CONFIRMED.value
                
                # Update addresses from DodoPayments data
                if hasattr(data, 'billing') and data.billing:
                    order.billing_address = self._format_address_dict(data.billing)
                elif hasattr(data, 'billing_address') and data.billing_address:
                    order.billing_address = self._format_address(data.billing_address)
                
                if hasattr(data, 'shipping_address') and data.shipping_address:
                    order.shipping_address = self._format_address(data.shipping_address)
                elif order.billing_address:
                    # Use billing address as shipping address if no separate shipping address
                    order.shipping_address = order.billing_address
                
                self.session.commit()
                
                return {
                    "status": "processed",
                    "action": "order_confirmed",
                    "order_id": str(order.id)
                }
            else:
                return {
                    "status": "ignored",
                    "reason": f"Order already in status: {order.status}"
                }
        
        # No existing order - create new order from cart items
        # Get user
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get cart items
        cart_items = self.session.query(CartItem).filter(CartItem.user_id == user_id).all()
        if not cart_items:
            return {
                "status": "ignored",
                "reason": "No cart items found for user"
            }
        
        # Calculate total amount and prepare order items
        total_amount = Decimal('0')
        order_items_data = []
        
        for cart_item in cart_items:
            product = cart_item.product
            item_total = product.price * cart_item.quantity
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'quantity': cart_item.quantity,
                'price_at_time': product.price
            })
        
        # Create order with addresses from payment data
        billing_address = ""
        shipping_address = ""
        
        # Handle billing address from actual webhook format
        if hasattr(data, 'billing') and data.billing:
            billing_address = self._format_address_dict(data.billing)
        elif hasattr(data, 'billing_address') and data.billing_address:
            billing_address = self._format_address(data.billing_address)
        
        if hasattr(data, 'shipping_address') and data.shipping_address:
            shipping_address = self._format_address(data.shipping_address)
        elif billing_address:
            # Use billing address as shipping address if no separate shipping address
            shipping_address = billing_address
        
        new_order = Order(
            user_id=user_id,
            status=OrderStatus.CONFIRMED.value,  # Payment already succeeded
            total_amount=total_amount,
            shipping_address=shipping_address,
            billing_address=billing_address
        )
        
        self.session.add(new_order)
        self.session.flush()  # Get order ID
        
        # Create order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=new_order.id,
                **item_data
            )
            self.session.add(order_item)
        
        # Clear cart items since payment was successful
        self.session.query(CartItem).filter(CartItem.user_id == user_id).delete()
        
        self.session.commit()
        
        return {
            "status": "processed",
            "action": "order_created",
            "order_id": str(new_order.id)
        }

    def _handle_payment_failed(self, order: Order, data: Any, user_id: int) -> Dict[str, Any]:
        """Handle failed payment"""
        
        # If order exists, update status to cancelled
        if order and order.status == OrderStatus.PENDING.value:
            order.status = OrderStatus.CANCELLED.value
            self.session.commit()
            
            return {
                "status": "processed",
                "action": "order_cancelled",
                "order_id": str(order.id)
            }
        
        # If no order exists, just return success (cart items remain for retry)
        if not order:
            return {
                "status": "processed",
                "action": "payment_failed_no_order",
                "reason": "Payment failed, cart items preserved for retry"
            }
        
        return {
            "status": "ignored",
            "reason": f"Order already in status: {order.status}"
        }

    def _handle_payment_refunded(self, order: Order, data: Any, user_id: int) -> Dict[str, Any]:
        """Handle payment refund"""
        
        # Only handle refunds if order exists
        if not order:
            return {
                "status": "ignored",
                "reason": "No order found for refund"
            }
        
        # Update order status to cancelled if refunded
        if order.status in [OrderStatus.CONFIRMED.value, OrderStatus.SHIPPED.value]:
            order.status = OrderStatus.CANCELLED.value
            self.session.commit()
            
            return {
                "status": "processed",
                "action": "order_refunded",
                "order_id": str(order.id)
            }
        
        return {
            "status": "ignored",
            "reason": f"Order in status: {order.status}, cannot refund"
        }
    
    def _format_address(self, address) -> str:
        """Format address object into a string"""
        if not address:
            return ""
        
        parts = []
        if hasattr(address, 'line1') and address.line1:
            parts.append(address.line1)
        if hasattr(address, 'line2') and address.line2:
            parts.append(address.line2)
        if hasattr(address, 'city') and address.city:
            parts.append(address.city)
        if hasattr(address, 'state') and address.state:
            parts.append(address.state)
        if hasattr(address, 'postal_code') and address.postal_code:
            parts.append(address.postal_code)
        if hasattr(address, 'country') and address.country:
            parts.append(address.country)
        
        return ", ".join(parts)
    
    def _format_address_dict(self, address_dict) -> str:
        """Format address dictionary into a string"""
        if not address_dict or not isinstance(address_dict, dict):
            return ""
        
        parts = []
        # Handle DodoPayments webhook address format
        if address_dict.get('street'):
            parts.append(address_dict['street'])
        if address_dict.get('city'):
            parts.append(address_dict['city'])
        if address_dict.get('state'):
            parts.append(address_dict['state'])
        if address_dict.get('zipcode'):
            parts.append(address_dict['zipcode'])
        if address_dict.get('country'):
            parts.append(address_dict['country'])
        
        return ", ".join(parts)
