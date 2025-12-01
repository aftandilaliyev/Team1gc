from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from passlib.context import CryptContext

from .base import Base

if TYPE_CHECKING:
    from .payments import Customer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    role: Mapped[str] = mapped_column(server_default='user')
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="user")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
