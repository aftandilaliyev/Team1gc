from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ProductImageBase(BaseModel):
    image_url: str = Field(..., max_length=255)


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageResponse(ProductImageBase):
    id: UUID
    product_id: UUID
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    description: Optional[str] = None


class ProductCreate(ProductBase):
    type_id: UUID
    images: List[ProductImageCreate] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    description: Optional[str] = None
    type_id: Optional[UUID] = None


class ProductResponse(ProductBase):
    id: UUID
    seller_id: UUID
    type_id: UUID
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
    category: Optional[UUID] = None
    search: Optional[str] = Field(default=None, max_length=255)
    sort: Optional[str] = Field(default="created_at", pattern="^(name|price|created_at)$")
    order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")
