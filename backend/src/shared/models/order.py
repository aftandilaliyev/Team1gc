from sqlalchemy.orm import Mapped, relationship

from backend.src.shared.models.base import Base


class OrderedProduct(Base):
    __tablename__ = "product_in_cart"

    id: Mapped[int]
    order_id: Mapped[int] # NOTE: having order_id null means it's in cart
    user_id: Mapped[int]
    product_id: Mapped[int]
    quantity: Mapped[int]

    order: Mapped["Order"] = relationship("Order", back_populates="products")


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int]
    user_id: Mapped[int]

    products: Mapped["OrderedProduct"] = relationship("OrderedProduct", back_populates="order")
