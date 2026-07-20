from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_model import TimestampMixin


class ProcessedRequest(Base, TimestampMixin):
    """
    Stores processed requests to support idempotency.
    """

    __tablename__ = "processed_requests"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    request_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    tool_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    response_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    response_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"<ProcessedRequest("
            f"request_id='{self.request_id}', "
            f"tool='{self.tool_name}')>"
        )