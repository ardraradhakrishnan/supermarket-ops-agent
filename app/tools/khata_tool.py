from app.database.database import SessionLocal

from app.schemas.khata import (
    KhataTransactionCreate,
)

from app.services.khata_service import KhataService

from app.utils.serializers import (
    serialize_customer,
    serialize_customers,
    serialize_khata_transaction,
    serialize_khata_transactions,
)


def add_credit(
    transaction: KhataTransactionCreate,
) -> dict:
    """
    Records a customer credit transaction.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        khata = service.add_credit(
            transaction
        )

        service.commit()

        return serialize_khata_transaction(
            khata
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()


def add_payment(
    transaction: KhataTransactionCreate,
) -> dict:
    """
    Records a customer payment.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        khata = service.add_payment(
            transaction
        )

        service.commit()

        return serialize_khata_transaction(
            khata
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()


def get_balance(
    customer_id: int,
) -> dict:
    """
    Returns customer's outstanding balance.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        return {
            "customer_id": customer_id,
            "balance": float(
                service.get_balance(
                    customer_id
                )
            ),
        }

    finally:

        db.close()


def get_ledger(
    customer_id: int,
) -> list[dict]:
    """
    Returns customer's complete ledger.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        ledger = service.get_ledger(
            customer_id
        )

        return serialize_khata_transactions(
            ledger
        )

    finally:

        db.close()


def clear_balance(
    customer_id: int,
):
    """
    Clears customer's outstanding balance.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        transaction = service.clear_balance(
            customer_id
        )

        service.commit()

        if transaction is None:

            return {
                "message": "Customer has no outstanding balance."
            }

        return serialize_khata_transaction(
            transaction
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()


def search_customer_ledger(
    keyword: str,
):
    """
    Search customer ledger by customer name or phone.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        customers = service.search_customer_ledger(
            keyword
        )

        return serialize_customers(
            customers
        )

    finally:

        db.close()


def list_pending_customers():
    """
    Returns customers having outstanding balances.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        pending = service.list_pending_customers()

        return [
            {
                "customer": serialize_customer(
                    item["customer"]
                ),
                "balance": float(
                    item["balance"]
                ),
            }
            for item in pending
        ]

    finally:

        db.close()


def get_total_outstanding():
    """
    Returns total outstanding amount.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        return {
            "total_outstanding": float(
                service.get_total_outstanding()
            )
        }

    finally:

        db.close()


def get_top_debtors(
    limit: int = 10,
):
    """
    Returns customers with the highest outstanding balances.
    """

    db = SessionLocal()

    try:

        service = KhataService(db)

        debtors = service.get_top_debtors(
            limit
        )

        return [
            {
                "customer": serialize_customer(
                    item["customer"]
                ),
                "balance": float(
                    item["balance"]
                ),
            }
            for item in debtors
        ]

    finally:

        db.close()