from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.shared.dependencies.auth import get_current_user
from src.shared.models.user import User
from src.shared.schemas.order import OrderResponse, OrderUpdate
from .service import SupplierService

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("/orders/pending", response_model=List[OrderResponse])
def get_orders_for_approval(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get orders that need supplier approval"""
    service = SupplierService(db)
    return service.get_orders_for_approval(current_user.id, page, per_page)


@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all orders (suppliers can view all orders)"""
    service = SupplierService(db)
    return service.get_all_orders(current_user.id, page, per_page)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order details"""
    service = SupplierService(db)
    return service.get_order_by_id(current_user.id, order_id)


@router.post("/orders/{order_id}/approve", response_model=OrderResponse)
def approve_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve an order (move from confirmed to shipped)"""
    service = SupplierService(db)
    return service.approve_order(current_user.id, order_id)


@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    status_update: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update order status (ship, deliver, cancel)"""
    service = SupplierService(db)
    return service.update_order_status(current_user.id, order_id, status_update)


@router.get("/analytics")
def get_supplier_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get supplier analytics dashboard data"""
    service = SupplierService(db)
    return service.get_supplier_analytics(current_user.id)
