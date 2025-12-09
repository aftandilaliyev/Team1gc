from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.shared.dependencies.auth import get_current_user
from src.shared.models.user import User
from src.shared.schemas.product import ProductResponse, ProductListResponse, ProductQueryParams
from src.shared.schemas.order import (
    CartItemCreate, CartItemResponse, CartItemUpdate, CartItemWithProductResponse,
    CheckoutRequest, CheckoutResponse, OrderResponse
)
from .service import BuyerService

router = APIRouter(prefix="/buyers", tags=["buyers"])


@router.get("/products", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    price_min: float = Query(None, ge=0),
    price_max: float = Query(None, ge=0),
    product_type: str = Query(None),
    search: str = Query(None),
    sort: str = Query("created_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """Get paginated list of products with filtering"""
    params = ProductQueryParams(
        page=page,
        per_page=per_page,
        price_min=price_min,
        price_max=price_max,
        product_type=product_type,
        search=search,
        sort=sort,
        order=order
    )
    
    service = BuyerService(db)
    return service.get_products(params)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get a single product by ID"""
    service = BuyerService(db)
    return service.get_product_by_id(product_id)


@router.post("/cart")
def add_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    service = BuyerService(db)
    return service.add_to_cart(current_user.id, item_data)


@router.get("/cart", response_model=List[CartItemWithProductResponse])
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's cart items"""
    service = BuyerService(db)
    return service.get_cart(current_user.id)


@router.put("/cart/{item_id}", response_model=CartItemResponse)
def update_cart_item(
    item_id: str,
    update_data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    service = BuyerService(db)
    return service.update_cart_item(current_user.id, item_id, update_data)


@router.delete("/cart/{item_id}")
def remove_from_cart(
    item_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    service = BuyerService(db)
    service.remove_from_cart(current_user.id, item_id)
    return {"message": "Item removed from cart"}


@router.delete("/cart")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    service = BuyerService(db)
    service.clear_cart(current_user.id)
    return {"message": "Cart cleared"}


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(
    checkout_data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process checkout and create order"""
    service = BuyerService(db)
    return service.checkout(current_user.id, checkout_data)


@router.get("/orders", response_model=List[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's order history"""
    service = BuyerService(db)
    return service.get_orders(current_user.id)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order details"""
    service = BuyerService(db)
    return service.get_order_by_id(current_user.id, order_id)
