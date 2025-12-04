from typing import TYPE_CHECKING
from sqlalchemy import String, Numeric, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4

from src.infrastructure.database import Base
if TYPE_CHECKING:
    from .user import User


class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    seller_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("product_types.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(12,2), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    images: Mapped[list["ProductImage"]] = relationship("ProductImage", cascade="all, delete-orphan")
    seller: Mapped["User"] = relationship("User", foreign_keys=[seller_id], back_populates="products")


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
