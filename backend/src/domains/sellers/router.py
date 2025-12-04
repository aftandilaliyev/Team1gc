from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.shared.dependencies.auth import get_current_user
from src.shared.models.user import User
from src.shared.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
)
from src.shared.schemas.order import OrderResponse, OrderUpdate
from .service import SellerService

router = APIRouter(prefix="/sellers", tags=["sellers"])


@router.post("/products", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product"""
    service = SellerService(db)
    return service.create_product(current_user.id, product_data)


@router.get("/products", response_model=ProductListResponse)
def get_seller_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all products for the current seller"""
    service = SellerService(db)
    return service.get_seller_products(current_user.id, page, per_page)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    service = SellerService(db)
    return service.get_product_by_id(current_user.id, product_id)


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    update_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a product"""
    service = SellerService(db)
    return service.update_product(current_user.id, product_id, update_data)


@router.delete("/products/{product_id}")
def delete_product(
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a product"""
    service = SellerService(db)
    service.delete_product(current_user.id, product_id)
    return {"message": "Product deleted successfully"}


@router.get("/orders", response_model=List[OrderResponse])
def get_seller_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get orders containing seller's products"""
    service = SellerService(db)
    return service.get_seller_orders(current_user.id, page, per_page)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order details"""
    service = SellerService(db)
    return service.get_order_by_id(current_user.id, order_id)


@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: UUID,
    status_update: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update order status (approve/ship orders)"""
    service = SellerService(db)
    return service.update_order_status(current_user.id, order_id, status_update)


@router.get("/analytics")
def get_seller_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get seller analytics dashboard data"""
    service = SellerService(db)
    return service.get_seller_analytics(current_user.id)
