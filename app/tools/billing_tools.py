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

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

    finally:

        db.close()


def _resolve_bill(service: BillingService, bill_identifier: int | str):
    """
    Helper to resolve a bill by ID (int or numeric str) or invoice number.
    """
    if isinstance(bill_identifier, int):
        return service.get_bill(bill_identifier)
    
    bill_str = str(bill_identifier).strip()
    if bill_str.isdigit():
        return service.get_bill(int(bill_str))
    else:
        return service.get_bill_by_invoice(bill_str)


def get_bill(
    bill_id: int | str,
) -> dict:
    """
    Returns a bill by ID (int) or invoice number (str).
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        bill = _resolve_bill(service, bill_id)

        return serialize_bill(
            bill
        )

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

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

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

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

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

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

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

    finally:

        db.close()


def cancel_bill(
    bill_id: int | str,
):
    """
    Cancels a bill by bill ID (int) or invoice number (str).
    """

    db = SessionLocal()

    try:

        service = BillingService(db)

        target_bill = _resolve_bill(service, bill_id)

        bill = service.cancel_bill(
            target_bill.id
        )

        return serialize_bill(
            bill
        )

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

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

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }

    finally:

        db.close()


def generate_invoice_pdf(
    bill_id: int | str,
) -> dict:
    """
    Generates a PDF (or HTML fallback) invoice for the given bill ID or invoice number.
    Returns a status dict containing the absolute file path.
    """

    db = SessionLocal()

    try:
        from app.services.billing_service import BillingService
        from app.services.pdf_service import PDFService

        billing_service = BillingService(db)
        pdf_service = PDFService(db)

        bill = _resolve_bill(billing_service, bill_id)
        file_path = pdf_service.generate_invoice_pdf(bill)

        return {
            "status": "success",
            "message": f"Invoice {bill.invoice_number} generated.",
            "file_path": file_path,
            "invoice_number": bill.invoice_number,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to generate invoice PDF: {str(e)}",
        }

    finally:
        db.close()