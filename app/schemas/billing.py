from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import PaymentMethod


class BillItemCreate(BaseModel):
    """
    Single bill line item.
    """

    product_id: int
    quantity: Decimal


class BillCreate(BaseModel):
    """
    Schema for bill creation.
    """

    customer_id: int | None = None
    payment_method: PaymentMethod
    discount: Decimal = Decimal("0.00")
    items: list[BillItemCreate]


class BillItemResponse(BaseModel):
    """
    Bill item returned to clients.
    """

    id: int
    product_id: int
    quantity: Decimal
    unit_price: Decimal
    gst_amount: Decimal
    line_total: Decimal

    model_config = ConfigDict(from_attributes=True)


class BillResponse(BaseModel):
    """
    Bill returned to clients.
    """

    id: int
    invoice_number: str
    subtotal: Decimal
    gst_amount: Decimal
    discount: Decimal
    grand_total: Decimal
    items: list[BillItemResponse]

    model_config = ConfigDict(from_attributes=True)




class BillPaymentCreate(BaseModel):
    """
    Schema for recording bill payments.
    """

    bill_id: int
    amount: Decimal
    payment_method: PaymentMethod