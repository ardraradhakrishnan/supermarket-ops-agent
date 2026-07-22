from app.database.database import SessionLocal

from app.schemas.billing import (
    BillCreate,
    BillPaymentCreate,
)

from app.services.billing_service import BillingService

from app.utils.serializers import (
    serialize_bill,
    serialize_bills,
)


def create_bill(
    bill: BillCreate,
) -> dict:
    """
    Creates a new bill.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        new_bill = service.create_bill(
            bill
        )

        return serialize_bill(
            new_bill
        )

    finally:

        db.close()


def get_bill(
    bill_id: int,
) -> dict:
    """
    Returns a bill by id.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bill = service.get_bill(
            bill_id
        )

        return serialize_bill(
            bill
        )

    finally:

        db.close()


def get_bill_by_invoice(
    invoice_number: str,
) -> dict:
    """
    Returns a bill using invoice number.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bill = service.get_bill_by_invoice(
            invoice_number
        )

        return serialize_bill(
            bill
        )

    finally:

        db.close()


def list_bills():
    """
    Returns all bills.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bills = service.list_bills()

        return serialize_bills(
            bills
        )

    finally:

        db.close()


def search_bill(
    keyword: str,
):
    """
    Search bills by invoice number,
    customer name or phone.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bills = service.search_bill(
            keyword
        )

        return serialize_bills(
            bills
        )

    finally:

        db.close()


def cancel_bill(
    bill_id: int,
):
    """
    Cancels a bill.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bill = service.cancel_bill(
            bill_id
        )

        return serialize_bill(
            bill
        )

    finally:

        db.close()


def receive_payment(
    payment: BillPaymentCreate,
):
    """
    Records payment for a bill.
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bill = service.receive_payment(
            payment
        )

        return serialize_bill(
            bill
        )

    finally:

        db.close()