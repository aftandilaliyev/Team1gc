from datetime import datetime
from enum import StrEnum
from typing import List, Optional
from pydantic import BaseModel, Field

from src.shared.schemas.product import ProductBase, ProductWithImages
# from src.shared.schemas.product import ProductBase


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class CartItemBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(CartItemBase):
    id: str
    user_id: int
    
    class Config:
        from_attributes = True

class CartItemWithProductResponse(CartItemBase):
    id: str
    user_id: int
    product: ProductWithImages | None = None
    
    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    price_at_time: float
    product: ProductWithImages | None = None
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.PENDING


class OrderCreate(OrderBase):
    items: List[CartItemCreate]
    shipping_address: str
    billing_address: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None


class OrderResponse(OrderBase):
    id: str
    user_id: int
    total_amount: float
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class CheckoutRequest(BaseModel):
    pass
    # shipping_address: str
    # billing_address: Optional[str] = None
    # payment_method: str = "dodo_payments"


class CheckoutResponse(BaseModel):
    order_id: Optional[str] = None
    payment_url: Optional[str] = None
    total_amount: float
    status: str
