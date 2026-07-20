from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin
from app.models.enums import InventoryTransactionType


class InventoryTransaction(Base, TimestampMixin):

    __tablename__ = "inventory_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    transaction_type: Mapped[InventoryTransactionType] = mapped_column(
        SqlEnum(InventoryTransactionType),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    reference: Mapped[str | None] = mapped_column(
        String(100),
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
    )

    product: Mapped["Product"] = relationship(
        back_populates="inventory_transactions",
    )