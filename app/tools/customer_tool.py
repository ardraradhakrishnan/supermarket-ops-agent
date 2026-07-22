from app.database.database import SessionLocal

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
)

from app.services.customer_service import CustomerService

from app.utils.serializers import (
    serialize_customer,
    serialize_customers,
)


def search_customer(
    keyword: str,
) -> list[dict]:
    """
    Search customers by name or phone.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customers = service.search(
            keyword
        )

        return serialize_customers(
            customers
        )

    finally:

        db.close()


def list_customers():
    """
    Returns all active customers.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customers = service.list()

        return serialize_customers(
            customers
        )

    finally:

        db.close()


def get_customer(
    customer_id: int,
) -> dict:
    """
    Returns a customer by id.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customer = service.get(
            customer_id
        )

        return serialize_customer(
            customer
        )

    finally:

        db.close()


def get_walkin_customer():
    """
    Returns the default walk-in customer.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customer = service.get_walkin_customer()

        return serialize_customer(
            customer
        )

    finally:

        db.close()


def create_customer(
    customer: CustomerCreate,
) -> dict:
    """
    Creates a customer.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        new_customer = service.create(
            customer
        )

        service.commit()

        return serialize_customer(
            new_customer
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()


def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
) -> dict:
    """
    Updates a customer.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        updated = service.update(
            customer_id,
            customer,
        )

        service.commit()

        return serialize_customer(
            updated
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()


def deactivate_customer(
    customer_id: int,
) -> dict:
    """
    Deactivates a customer.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customer = service.deactivate(
            customer_id,
        )

        service.commit()

        return serialize_customer(
            customer
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()


def get_customer_by_phone(
    phone: str,
) -> dict:
    """
    Returns a customer using phone number.
    """

    db = SessionLocal()

    try:

        service = CustomerService(db)

        customer = service.get_by_phone(
            phone
        )

        if customer is None:
            return {}

        return serialize_customer(
            customer
        )

    finally:

        db.close()