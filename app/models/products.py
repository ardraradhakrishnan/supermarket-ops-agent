from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin
from app.models.enums import Unit


class Product(Base, TimestampMixin):
    """
    Master table for all supermarket products.
    """

    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "gst_rate IN (0, 5, 12, 18, 28)",
            name="ck_product_gst_rate",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Stock Keeping Unit",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    gst_rate: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit: Mapped[Unit] = mapped_column(
        SqlEnum(Unit),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("1"),
        nullable=False,
    )

    inventory_transactions: Mapped[list["InventoryTransaction"]] = relationship(
        back_populates="product",
        lazy="selectin",
    )

    bill_items: Mapped[list["BillItem"]] = relationship(
        back_populates="product",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<Product(id={self.id}, "
            f"sku='{self.sku}', "
            f"name='{self.name}')>"
        )