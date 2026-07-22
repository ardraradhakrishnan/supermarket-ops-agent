from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import Unit


class ProductBase(BaseModel):
    """
    Shared product fields.
    """

    sku: str
    name: str
    description: str | None = None
    unit_price: Decimal
    gst_rate: int
    unit: Unit
    is_active: bool = True


class ProductCreate(ProductBase):
    """
    Schema for creating a product.
    """

    pass


class ProductUpdate(BaseModel):
    """
    Schema for updating a product.
    """

    sku: str | None = None
    name: str | None = None
    description: str | None = None
    unit_price: Decimal | None = None
    gst_rate: int | None = None
    unit: Unit | None = None
    is_active: bool | None = None


class ProductResponse(ProductBase):
    """
    Schema returned to clients.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)