from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductImageBase(BaseModel):
    image_url: str = Field(..., max_length=255)


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: str
    product_id: str
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    description: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    product_type: Optional[str] = Field(None, max_length=100)
    images: List[ProductImageCreate] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    description: Optional[str] = None
    product_type: Optional[str] = Field(None, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    id: str
    seller_id: int
    product_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageResponse] = []
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class ProductQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    price_min: Optional[Decimal] = Field(default=None, ge=0)
    price_max: Optional[Decimal] = Field(default=None, ge=0)
    product_type: Optional[str] = Field(default=None, max_length=100)
    search: Optional[str] = Field(default=None, max_length=255)
    sort: Optional[str] = Field(default="created_at", pattern="^(name|price|created_at)$")
    order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")
