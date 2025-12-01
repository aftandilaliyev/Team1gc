from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.shared.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
        nullable=False
    )
    customer_id: Mapped[str] = mapped_column(String(255), nullable=False)
    billing_email: Mapped[str] = mapped_column(String(255), nullable=False)
    billing_name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="customer")
