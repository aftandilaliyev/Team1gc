import io
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.infrastructure.bucket import R2BucketManager
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


@router.post("/products/with-images", response_model=ProductResponse)
async def create_product_with_images(
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    stock_quantity: int = Form(default=0),
    product_type: Optional[str] = Form(None),
    images: List[UploadFile] = File(default=[]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product with image uploads"""
    try:
        # Validate images
        if len(images) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 images allowed")
        
        # Upload images to R2
        image_urls = []
        if images and images[0].filename:  # Check if files were actually uploaded
            bucket_manager = R2BucketManager()
            
            for image in images:
                if image.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Invalid image type: {image.content_type}"
                    )
                
                # Read and upload image
                content = await image.read()
                file_buffer = io.BytesIO(content)
                
                file_key = await bucket_manager.put(
                    path="products/images",
                    file_buffer=file_buffer,
                    content_type=image.content_type,
                    file_type=image.content_type
                )
                
                # Get public URL
                public_url = bucket_manager.get_public_url(file_key)
                image_urls.append(public_url)
        
        # Create product data
        from src.shared.schemas.product import ProductImageCreate
        product_images = [ProductImageCreate(image_url=url) for url in image_urls]
        
        product_data = ProductCreate(
            name=name,
            price=price,
            description=description,
            stock_quantity=stock_quantity,
            product_type=product_type,
            images=product_images
        )
        
        # Create product
        service = SellerService(db)
        return service.create_product(current_user.id, product_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")


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
