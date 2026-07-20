from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin
from app.models.enums import KhataTransactionType


class KhataTransaction(Base, TimestampMixin):
    """
    Stores customer credit (Khata) transactions.
    """

    __tablename__ = "khata_transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    bill_id: Mapped[int | None] = mapped_column(
        ForeignKey("bills.id"),
        nullable=True,
        index=True,
    )

    transaction_type: Mapped[KhataTransactionType] = mapped_column(
        SqlEnum(KhataTransactionType),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    balance_after: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="khata_transactions",
        lazy="selectin",
    )

    bill: Mapped["Bill"] = relationship(
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<KhataTransaction("
            f"customer_id={self.customer_id}, "
            f"type='{self.transaction_type.value}', "
            f"amount={self.amount})>"
        )