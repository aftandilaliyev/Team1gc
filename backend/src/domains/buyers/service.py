from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from fastapi import HTTPException, status

from src.shared.models.product import Product, ProductImage
from src.shared.models.order import CartItem, Order, OrderItem, OrderStatus
from src.shared.models.user import User
from src.shared.models.payments import Customer
from src.shared.schemas.product import ProductResponse, ProductListResponse, ProductQueryParams
from src.shared.schemas.order import (
    CartItemCreate, CartItemResponse, CartItemUpdate,
    CheckoutRequest, CheckoutResponse, OrderResponse
)
from src.infrastructure.payments import DodoPaymentsService


class BuyerService:
    def __init__(self, session: Session):
        self.session = session
        self.dodo_payments = DodoPaymentsService()

    def get_products(self, params: ProductQueryParams) -> ProductListResponse:
        """Get paginated list of products with filtering and sorting"""
        query = self.session.query(Product)
        
        # Apply filters
        if params.price_min is not None:
            query = query.filter(Product.price >= params.price_min)
        
        if params.price_max is not None:
            query = query.filter(Product.price <= params.price_max)
        
        if params.category:
            query = query.filter(Product.type_id == params.category)
        
        if params.search:
            search_term = f"%{params.search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Apply sorting
        sort_column = getattr(Product, params.sort, Product.created_at)
        if params.order == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (params.page - 1) * params.per_page
        products = query.offset(offset).limit(params.per_page).all()
        
        # Calculate total pages
        total_pages = (total + params.per_page - 1) // params.per_page
        
        return ProductListResponse(
            products=[ProductResponse.model_validate(product) for product in products],
            total=total,
            page=params.page,
            per_page=params.per_page,
            total_pages=total_pages
        )

    def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        """Get a single product by ID"""
        product = self.session.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        return ProductResponse.model_validate(product)

    def add_to_cart(self, user_id: int, item_data: CartItemCreate) -> CartItemResponse:
        """Add item to user's cart"""
        # Check if product exists
        product = self.session.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Check if item already in cart
        existing_item = self.session.query(CartItem).filter(
            and_(
                CartItem.user_id == user_id,
                CartItem.product_id == item_data.product_id
            )
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += item_data.quantity
            self.session.commit()
            self.session.refresh(existing_item)
            return CartItemResponse.model_validate(existing_item)
        else:
            # Create new cart item
            cart_item = CartItem(
                user_id=user_id,
                product_id=item_data.product_id,
                quantity=item_data.quantity
            )
            self.session.add(cart_item)
            self.session.commit()
            self.session.refresh(cart_item)
            return CartItemResponse.model_validate(cart_item)

    def get_cart(self, user_id: int) -> List[CartItemResponse]:
        """Get user's cart items"""
        cart_items = self.session.query(CartItem).filter(CartItem.user_id == user_id).all()
        return [CartItemResponse.model_validate(item) for item in cart_items]

    def update_cart_item(self, user_id: int, item_id: UUID, update_data: CartItemUpdate) -> CartItemResponse:
        """Update cart item quantity"""
        cart_item = self.session.query(CartItem).filter(
            and_(
                CartItem.id == item_id,
                CartItem.user_id == user_id
            )
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        cart_item.quantity = update_data.quantity
        self.session.commit()
        self.session.refresh(cart_item)
        return CartItemResponse.model_validate(cart_item)

    def remove_from_cart(self, user_id: int, item_id: UUID) -> None:
        """Remove item from cart"""
        cart_item = self.session.query(CartItem).filter(
            and_(
                CartItem.id == item_id,
                CartItem.user_id == user_id
            )
        ).first()
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        
        self.session.delete(cart_item)
        self.session.commit()

    def clear_cart(self, user_id: int) -> None:
        """Clear all items from user's cart"""
        self.session.query(CartItem).filter(CartItem.user_id == user_id).delete()
        self.session.commit()

    async def checkout(self, user_id: int, checkout_data: CheckoutRequest) -> CheckoutResponse:
        """Process checkout and create order with payment"""
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )
        
        # Calculate total amount
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
        
        # Create order
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING.value,
            total_amount=total_amount,
            shipping_address=checkout_data.shipping_address,
            billing_address=checkout_data.billing_address or checkout_data.shipping_address
        )
        
        self.session.add(order)
        self.session.flush()  # Get order ID
        
        # Create order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            self.session.add(order_item)
        
        # Get or create customer in payment system
        customer = self.session.query(Customer).filter(Customer.user_id == user_id).first()
        
        if not customer:
            # Create customer in DodoPayments
            dodo_customer = await self.dodo_payments.create_customer(
                email=user.email,
                name=user.username,
                user_id=user_id
            )
            
            # Save customer locally
            customer = Customer(
                user_id=user_id,
                customer_id=dodo_customer['id'],
                billing_email=user.email,
                billing_name=user.username
            )
            self.session.add(customer)
        
        # Create payment intent
        payment_intent = await self.dodo_payments.create_payment_intent(
            amount=total_amount,
            order_id=order.id,
            customer_email=customer.billing_email,
            customer_name=customer.billing_name,
            metadata={
                'user_id': str(user_id),
                'order_id': str(order.id)
            }
        )
        
        # Clear cart after successful order creation
        self.session.query(CartItem).filter(CartItem.user_id == user_id).delete()
        
        self.session.commit()
        
        return CheckoutResponse(
            order_id=order.id,
            payment_url=payment_intent.get('checkout_url'),
            total_amount=float(total_amount),
            status="payment_pending"
        )

    def get_orders(self, user_id: int) -> List[OrderResponse]:
        """Get user's order history"""
        orders = self.session.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).all()
        return [OrderResponse.model_validate(order) for order in orders]

    def get_order_by_id(self, user_id: int, order_id: UUID) -> OrderResponse:
        """Get specific order by ID"""
        order = self.session.query(Order).filter(
            and_(
                Order.id == order_id,
                Order.user_id == user_id
            )
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        return OrderResponse.model_validate(order)
