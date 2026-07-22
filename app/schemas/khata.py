from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import KhataTransactionType


class KhataTransactionBase(BaseModel):
    """
    Shared khata transaction fields.
    """

    customer_id: int
    transaction_type: KhataTransactionType
    amount: Decimal
    remarks: str | None = None


class KhataTransactionCreate(KhataTransactionBase):
    """
    Schema for creating khata transactions.
    """

    pass


class KhataTransactionResponse(KhataTransactionBase):
    """
    Schema returned to clients.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)