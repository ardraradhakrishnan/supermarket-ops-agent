from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import InventoryTransactionType


class InventoryTransactionBase(BaseModel):
    """
    Shared inventory transaction fields.
    """

    product_id: int
    transaction_type: InventoryTransactionType
    quantity: Decimal
    reference: str | None = None
    remarks: str | None = None


class InventoryTransactionCreate(InventoryTransactionBase):
    """
    Schema for creating inventory transactions.
    """

    pass


class InventoryTransactionResponse(InventoryTransactionBase):
    """
    Schema returned to clients.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)