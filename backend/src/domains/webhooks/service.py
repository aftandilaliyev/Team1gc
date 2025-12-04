from typing import Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.shared.models.order import Order, OrderStatus
from src.shared.schemas.payment import WebhookRequest
from src.infrastructure.payments import DodoPaymentsService


class WebhookService:
    def __init__(self, session: Session):
        self.session = session
        self.dodo_payments = DodoPaymentsService()

    async def handle_dodo_payment_webhook(
        self, 
        payload: bytes, 
        signature: str, 
        webhook_data: WebhookRequest
    ) -> Dict[str, Any]:
        """Handle DodoPayments webhook events"""
        
        # Verify webhook signature
        if not self.dodo_payments.verify_webhook_signature(payload, signature):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook signature"
            )
        
        event_type = webhook_data.event_type
        data = webhook_data.data
        
        # Extract order ID from metadata
        order_id = None
        if data.metadata and data.metadata.user_id:
            # Try to get order_id from metadata
            order_id = data.metadata.__dict__.get('order_id')
        
        if not order_id:
            # If no order_id in metadata, this might be a subscription webhook
            # For now, we'll just log and return success
            return {"status": "ignored", "reason": "No order_id in metadata"}
        
        try:
            order_uuid = UUID(order_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order ID format"
            )
        
        # Get the order
        order = self.session.query(Order).filter(Order.id == order_uuid).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Handle different event types
        if event_type == "payment.succeeded":
            return await self._handle_payment_succeeded(order, data)
        elif event_type == "payment.failed":
            return await self._handle_payment_failed(order, data)
        elif event_type == "payment.refunded":
            return await self._handle_payment_refunded(order, data)
        else:
            # Unknown event type, just log and return success
            return {"status": "ignored", "reason": f"Unknown event type: {event_type}"}

    async def _handle_payment_succeeded(self, order: Order, data: Any) -> Dict[str, Any]:
        """Handle successful payment"""
        
        # Update order status to confirmed if it's still pending
        if order.status == OrderStatus.PENDING.value:
            order.status = OrderStatus.CONFIRMED.value
            self.session.commit()
            
            return {
                "status": "processed",
                "action": "order_confirmed",
                "order_id": str(order.id)
            }
        
        return {
            "status": "ignored",
            "reason": f"Order already in status: {order.status}"
        }

    async def _handle_payment_failed(self, order: Order, data: Any) -> Dict[str, Any]:
        """Handle failed payment"""
        
        # Update order status to cancelled if payment failed
        if order.status == OrderStatus.PENDING.value:
            order.status = OrderStatus.CANCELLED.value
            self.session.commit()
            
            return {
                "status": "processed",
                "action": "order_cancelled",
                "order_id": str(order.id)
            }
        
        return {
            "status": "ignored",
            "reason": f"Order already in status: {order.status}"
        }

    async def _handle_payment_refunded(self, order: Order, data: Any) -> Dict[str, Any]:
        """Handle payment refund"""
        
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
