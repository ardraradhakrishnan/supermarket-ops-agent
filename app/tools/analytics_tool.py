from app.database.database import SessionLocal

from app.services.analytics_service import AnalyticsService


def get_dashboard_summary() -> dict:
    """
    Returns overall business dashboard summary.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_dashboard_summary()

    finally:

        db.close()


def get_sales_summary() -> dict:
    """
    Returns today's sales summary.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_sales_summary()

    finally:

        db.close()


def get_top_selling_products(
    limit: int = 10,
) -> list[dict]:
    """
    Returns the best selling products.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_top_selling_products(limit)

    finally:

        db.close()


def get_low_stock_report() -> list[dict]:
    """
    Returns products with low stock.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_low_stock_report()

    finally:

        db.close()


def get_customer_outstanding_report() -> list[dict]:
    """
    Returns customers with pending Khata balance.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_customer_outstanding_report()

    finally:

        db.close()


def get_inventory_value() -> dict:
    """
    Returns total inventory value.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_inventory_value()

    finally:

        db.close()


def get_recent_sales(
    limit: int = 10,
) -> list[dict]:
    """
    Returns recent bills.
    """

    db = SessionLocal()

    try:

        service = AnalyticsService(db)

        return service.get_recent_sales(limit)

    finally:

        db.close()