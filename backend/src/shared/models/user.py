from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from passlib.context import CryptContext

from src.infrastructure.database import Base

if TYPE_CHECKING:
    from .payments import Customer
    from .product import Product

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(Enum):
    BUYER = "buyer"
    SELLER = "seller"
    SUPPLIER = "supplier"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    email: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(
        server_default='1', default=True
    )
    role: Mapped[str] = mapped_column(server_default=UserRole.BUYER.value)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="user")
    products: Mapped["Product"] = relationship("Product", back_populates="seller")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
