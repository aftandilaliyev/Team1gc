from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from fastapi import HTTPException, status

from src.shared.models.product import Product, ProductImage
from src.shared.models.order import Order, OrderItem, OrderStatus
from src.shared.models.user import User, UserRole
from src.shared.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
)
from src.shared.schemas.order import OrderResponse, OrderUpdate


class SellerService:
    def __init__(self, session: Session):
        self.session = session

    def _verify_seller_access(self, user_id: int, product_id: Optional[UUID] = None) -> User:
        """Verify user is a seller and has access to the product if specified"""
        user = self.session.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role != UserRole.SELLER.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Seller role required."
            )
        
        if product_id:
            product = self.session.query(Product).filter(
                and_(
                    Product.id == product_id,
                    Product.seller_id == user_id
                )
            ).first()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found or access denied"
                )
        
        return user

    def create_product(self, user_id: int, product_data: ProductCreate) -> ProductResponse:
        """Create a new product"""
        self._verify_seller_access(user_id)
        
        # Create product
        product = Product(
            seller_id=user_id,
            name=product_data.name,
            price=product_data.price,
            description=product_data.description,
            type_id=product_data.type_id
        )
        
        self.session.add(product)
        self.session.flush()  # Get product ID
        
        # Add images if provided
        for image_data in product_data.images:
            image = ProductImage(
                product_id=product.id,
                image_url=image_data.image_url
            )
            self.session.add(image)
        
        self.session.commit()
        self.session.refresh(product)
        
        return ProductResponse.model_validate(product)

    def get_seller_products(self, user_id: int, page: int = 1, per_page: int = 20) -> ProductListResponse:
        """Get all products for a seller"""
        self._verify_seller_access(user_id)
        
        query = self.session.query(Product).filter(Product.seller_id == user_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        products = query.order_by(desc(Product.created_at)).offset(offset).limit(per_page).all()
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page
        
        return ProductListResponse(
            products=[ProductResponse.model_validate(product) for product in products],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )

    def get_product_by_id(self, user_id: int, product_id: UUID) -> ProductResponse:
        """Get a specific product by ID (seller must own it)"""
        self._verify_seller_access(user_id, product_id)
        
        product = self.session.query(Product).filter(
            and_(
                Product.id == product_id,
                Product.seller_id == user_id
            )
        ).first()
        
        return ProductResponse.model_validate(product)

    def update_product(self, user_id: int, product_id: UUID, update_data: ProductUpdate) -> ProductResponse:
        """Update a product"""
        self._verify_seller_access(user_id, product_id)
        
        product = self.session.query(Product).filter(
            and_(
                Product.id == product_id,
                Product.seller_id == user_id
            )
        ).first()
        
        # Update fields if provided
        if update_data.name is not None:
            product.name = update_data.name
        
        if update_data.price is not None:
            product.price = update_data.price
        
        if update_data.description is not None:
            product.description = update_data.description
        
        if update_data.type_id is not None:
            product.type_id = update_data.type_id
        
        self.session.commit()
        self.session.refresh(product)
        
        return ProductResponse.model_validate(product)

    def delete_product(self, user_id: int, product_id: UUID) -> None:
        """Delete a product"""
        self._verify_seller_access(user_id, product_id)
        
        # Check if product has any pending orders
        pending_orders = self.session.query(OrderItem).join(Order).filter(
            and_(
                OrderItem.product_id == product_id,
                Order.status.in_([OrderStatus.PENDING.value, OrderStatus.CONFIRMED.value])
            )
        ).first()
        
        if pending_orders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete product with pending orders"
            )
        
        product = self.session.query(Product).filter(
            and_(
                Product.id == product_id,
                Product.seller_id == user_id
            )
        ).first()
        
        self.session.delete(product)
        self.session.commit()

    def get_seller_orders(self, user_id: int, page: int = 1, per_page: int = 20) -> List[OrderResponse]:
        """Get orders containing seller's products"""
        self._verify_seller_access(user_id)
        
        # Get orders that contain products from this seller
        orders = self.session.query(Order).join(OrderItem).join(Product).filter(
            Product.seller_id == user_id
        ).order_by(desc(Order.created_at)).offset((page - 1) * per_page).limit(per_page).all()
        
        return [OrderResponse.model_validate(order) for order in orders]

    def get_order_by_id(self, user_id: int, order_id: UUID) -> OrderResponse:
        """Get specific order details (if it contains seller's products)"""
        self._verify_seller_access(user_id)
        
        # Check if order contains seller's products
        order = self.session.query(Order).join(OrderItem).join(Product).filter(
            and_(
                Order.id == order_id,
                Product.seller_id == user_id
            )
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or access denied"
            )
        
        return OrderResponse.model_validate(order)

    def update_order_status(self, user_id: int, order_id: UUID, status_update: OrderUpdate) -> OrderResponse:
        """Update order status (seller can only approve/ship orders)"""
        self._verify_seller_access(user_id)
        
        # Check if order contains seller's products
        order = self.session.query(Order).join(OrderItem).join(Product).filter(
            and_(
                Order.id == order_id,
                Product.seller_id == user_id
            )
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found or access denied"
            )
        
        # Sellers can only move orders to confirmed or shipped status
        allowed_statuses = [OrderStatus.CONFIRMED.value, OrderStatus.SHIPPED.value]
        
        if status_update.status and status_update.status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sellers can only confirm or ship orders"
            )
        
        # Check valid status transitions
        current_status = order.status
        new_status = status_update.status
        
        valid_transitions = {
            OrderStatus.PENDING.value: [OrderStatus.CONFIRMED.value],
            OrderStatus.CONFIRMED.value: [OrderStatus.SHIPPED.value]
        }
        
        if new_status and new_status not in valid_transitions.get(current_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {current_status} to {new_status}"
            )
        
        # Update order status
        if status_update.status:
            order.status = status_update.status
        
        self.session.commit()
        self.session.refresh(order)
        
        return OrderResponse.model_validate(order)

    def get_seller_analytics(self, user_id: int) -> dict:
        """Get basic analytics for seller"""
        self._verify_seller_access(user_id)
        
        # Total products
        total_products = self.session.query(Product).filter(Product.seller_id == user_id).count()
        
        # Total orders containing seller's products
        total_orders = self.session.query(Order).join(OrderItem).join(Product).filter(
            Product.seller_id == user_id
        ).distinct().count()
        
        # Revenue (completed orders only)
        completed_orders = self.session.query(Order).join(OrderItem).join(Product).filter(
            and_(
                Product.seller_id == user_id,
                Order.status.in_([OrderStatus.DELIVERED.value])
            )
        ).all()
        
        total_revenue = sum(float(order.total_amount) for order in completed_orders)
        
        # Pending orders
        pending_orders = self.session.query(Order).join(OrderItem).join(Product).filter(
            and_(
                Product.seller_id == user_id,
                Order.status == OrderStatus.PENDING.value
            )
        ).distinct().count()
        
        return {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "pending_orders": pending_orders
        }
