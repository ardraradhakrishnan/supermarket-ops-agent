from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_model import TimestampMixin


class Preference(Base, TimestampMixin):
    """
    Stores application preferences as key-value pairs.
    """

    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<Preference(key='{self.key}', value='{self.value}')>"
        )