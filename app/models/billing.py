from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Integer,
    Numeric,
    String,
    text
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin
from app.models.enums import BillStatus, PaymentMethod, PaymentStatus


class Bill(Base, TimestampMixin):
    """
    Stores invoice header information.
    """

    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    invoice_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
        index=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    gst_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        SqlEnum(PaymentMethod),
        nullable=False,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        SqlEnum(PaymentStatus),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="bills",
        lazy="selectin",
    )

    bill_items: Mapped[list["BillItem"]] = relationship(
        back_populates="bill",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    status: Mapped[BillStatus] = mapped_column(
        SqlEnum(BillStatus),
        nullable=False,
        default=BillStatus.ACTIVE,
    )

    def __repr__(self) -> str:
        return (
            f"<Bill("
            f"invoice='{self.invoice_number}', "
            f"total={self.grand_total})>"
        )


class BillItem(Base):
    """
    Stores individual products within a bill.
    """

    __tablename__ = "bill_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    bill_id: Mapped[int] = mapped_column(
        ForeignKey("bills.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    gst_rate: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    bill: Mapped["Bill"] = relationship(
        back_populates="bill_items",
        lazy="selectin",
    )

    product: Mapped["Product"] = relationship(
        back_populates="bill_items",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<BillItem("
            f"bill_id={self.bill_id}, "
            f"product_id={self.product_id}, "
            f"qty={self.quantity})>"
        )