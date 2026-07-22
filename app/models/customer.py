from sqlalchemy import Boolean, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin


class Customer(Base, TimestampMixin):
    """
    Stores customer information.
    """

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
        index=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("1"),
        nullable=False,
    )

    bills: Mapped[list["Bill"]] = relationship(
        back_populates="customer",
        lazy="selectin",
    )

    khata_transactions: Mapped[list["KhataTransaction"]] = relationship(
        back_populates="customer",
        lazy="selectin",
    )

    def __repr__(self):
        return (
            f"<Customer(id={self.id}, "
            f"name='{self.name}', "
            f"phone='{self.phone}')>"
        )