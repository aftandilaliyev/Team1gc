from typing import List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from fastapi import HTTPException, status

from src.shared.models.order import Order, OrderItem, OrderStatus
from src.shared.models.user import User, UserRole
from src.shared.schemas.order import OrderResponse, OrderUpdate
from src.shared.models.product import Product

class SupplierService:
    def __init__(self, session: Session):
        self.session = session

    def _verify_supplier_access(self, user_id: int) -> User:
        """Verify user is a supplier"""
        user = self.session.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role != UserRole.SUPPLIER.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Supplier role required."
            )
        
        return user

    def get_orders_for_approval(self, user_id: int, page: int = 1, per_page: int = 20) -> List[OrderResponse]:
        """Get orders that need supplier approval (confirmed orders)"""
        self._verify_supplier_access(user_id)
        
        # Get orders that are confirmed and need supplier approval
        orders = self.session.query(Order).filter(
            Order.status == OrderStatus.CONFIRMED.value
        ).options(joinedload(Order.items).options(joinedload(OrderItem.product).options(joinedload(Product.images)))).order_by(desc(Order.created_at)).offset((page - 1) * per_page).limit(per_page).all()
        
        return orders

    def get_all_orders(self, user_id: int, page: int = 1, per_page: int = 20) -> List[OrderResponse]:
        """Get all orders (suppliers can view all orders)"""
        self._verify_supplier_access(user_id)
        
        orders = self.session.query(Order).options(
            joinedload(Order.items).options(joinedload(OrderItem.product).options(joinedload(Product.images)))
        ).order_by(desc(Order.created_at)).offset((page - 1) * per_page).limit(per_page).all()
        
        return orders

    def get_order_by_id(self, user_id: int, order_id: str) -> OrderResponse:
        """Get specific order details"""
        self._verify_supplier_access(user_id)
        
        order = self.session.query(Order).options(joinedload(Order.items).options(joinedload(OrderItem.product).options(joinedload(Product.images)))).filter(Order.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return order

    def approve_order(self, user_id: int, order_id: str) -> OrderResponse:
        """Approve an order (move from confirmed to shipped)"""
        self._verify_supplier_access(user_id)
        
        order = self.session.query(Order).options(joinedload(Order.items).options(joinedload(OrderItem.product).options(joinedload(Product.images)))).filter(Order.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Suppliers can only approve confirmed orders
        if order.status != OrderStatus.CONFIRMED.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must be confirmed before supplier approval"
            )
        
        # Move order to shipped status
        order.status = OrderStatus.SHIPPED.value
        
        self.session.commit()
        self.session.refresh(order)
        
        return order

    def update_order_status(self, user_id: int, order_id: str, status_update: OrderUpdate) -> OrderResponse:
        """Update order status (suppliers have broader permissions)"""
        self._verify_supplier_access(user_id)
        
        order = self.session.query(Order).filter(Order.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        # Suppliers can move orders to shipped, delivered, or cancelled status
        allowed_statuses = [
            OrderStatus.SHIPPED.value,
            OrderStatus.DELIVERED.value,
            OrderStatus.CANCELLED.value
        ]
        
        if status_update.status and status_update.status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Suppliers can only ship, deliver, or cancel orders"
            )
        
        # Check valid status transitions
        current_status = order.status
        new_status = status_update.status
        
        valid_transitions = {
            OrderStatus.PENDING.value: [OrderStatus.CANCELLED.value],
            OrderStatus.CONFIRMED.value: [OrderStatus.SHIPPED.value, OrderStatus.CANCELLED.value],
            OrderStatus.SHIPPED.value: [OrderStatus.DELIVERED.value, OrderStatus.CANCELLED.value]
        }
        
        if new_status and new_status not in valid_transitions.get(current_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {current_status} to {new_status}"
            )
        
        # Update order status
        if status_update.status:
            order.status = status_update.status
        
        # Update addresses if provided (suppliers can update shipping info)
        if status_update.shipping_address:
            order.shipping_address = status_update.shipping_address
        
        if status_update.billing_address:
            order.billing_address = status_update.billing_address
        
        self.session.commit()
        self.session.refresh(order)
        
        return order

    def get_supplier_analytics(self, user_id: int) -> dict:
        """Get analytics for supplier dashboard"""
        self._verify_supplier_access(user_id)
        
        # Total orders
        total_orders = self.session.query(Order).count()
        
        # Orders by status
        pending_orders = self.session.query(Order).filter(Order.status == OrderStatus.PENDING.value).count()
        confirmed_orders = self.session.query(Order).filter(Order.status == OrderStatus.CONFIRMED.value).count()
        shipped_orders = self.session.query(Order).filter(Order.status == OrderStatus.SHIPPED.value).count()
        delivered_orders = self.session.query(Order).filter(Order.status == OrderStatus.DELIVERED.value).count()
        cancelled_orders = self.session.query(Order).filter(Order.status == OrderStatus.CANCELLED.value).count()
        
        # Total revenue (delivered orders only)
        delivered_order_objects = self.session.query(Order).filter(Order.status == OrderStatus.DELIVERED.value).all()
        total_revenue = sum(float(order.total_amount) for order in delivered_order_objects)
        
        return {
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "confirmed_orders": confirmed_orders,
            "shipped_orders": shipped_orders,
            "delivered_orders": delivered_orders,
            "cancelled_orders": cancelled_orders,
            "total_revenue": total_revenue,
            "orders_needing_approval": confirmed_orders  # Orders waiting for supplier approval
        }
