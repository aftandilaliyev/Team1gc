from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.shared.schemas.product import ProductResponse, ProductListResponse
from .service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    elements: int = Query(20, ge=1, le=100),
    price_min: float = Query(None, ge=0),
    price_max: float = Query(None, ge=0),
    category: UUID = Query(None),
    sort: str = Query("created_at"),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get paginated list of products with filtering"""
    service = ProductService(db)
    return service.query_products(
        page=page,
        elements=elements,
        price_min=price_min,
        price_max=price_max,
        category=category,
        sort=sort,
        search=search
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a single product by ID"""
    service = ProductService(db)
    return service.get_product_by_id(product_id)