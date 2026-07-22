from app.database.database import SessionLocal

from app.services.preference_service import PreferenceService


def get_store_name() -> str:
    """
    Returns the configured store name.
    """

    db = SessionLocal()

    try:

        service = PreferenceService(db)

        return service.get_store_name()

    finally:

        db.close()


def get_currency() -> str:
    """
    Returns the configured currency.
    """

    db = SessionLocal()

    try:

        service = PreferenceService(db)

        return service.get_currency()

    finally:

        db.close()


def get_low_stock_threshold() -> int:
    """
    Returns the configured low stock threshold.
    """

    db = SessionLocal()

    try:

        service = PreferenceService(db)

        return service.get_low_stock_threshold()

    finally:

        db.close()


def get_preference(
    key: str,
):
    """
    Returns the value of a preference.
    """

    db = SessionLocal()

    try:

        service = PreferenceService(db)

        return service.get(key)

    finally:

        db.close()


def update_preference(
    key: str,
    value: str,
):
    """
    Updates a preference value.
    """

    db = SessionLocal()

    try:

        service = PreferenceService(db)

        preference = service.set(
            key,
            value,
        )

        service.commit()

        return {
            "key": preference.key,
            "value": preference.value,
        }

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()