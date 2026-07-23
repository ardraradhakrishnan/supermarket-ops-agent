from app.database.database import SessionLocal
from app.services.analytics_service import AnalyticsService


def get_dashboard_summary() -> dict:
    """
    Returns overall business dashboard summary.
    """
    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        summary = service.get_dashboard_summary()
        
        # Convert Decimal values to float for JSON compatibility
        summary["today_sales"] = float(summary["today_sales"])
        summary["pending_khata"] = float(summary["pending_khata"])
        return summary
    finally:
        db.close()


def get_sales_summary() -> dict:
    """
    Returns today's sales summary.
    """
    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        summary = service.get_sales_summary()
        
        # Convert Decimal values to float
        summary["sales_amount"] = float(summary["sales_amount"])
        summary["average_bill"] = float(summary["average_bill"])
        return summary
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
        # Quantities in top selling products are Decimal (sums)
        products = service.get_top_selling_products(limit)
        for item in products:
            item["quantity"] = float(item["quantity"])
        return products
    finally:
        db.close()


def get_low_stock_report() -> list[dict]:
    """
    Returns products with low stock.
    """
    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        # Quantities are Decimal (stock levels)
        report = service.get_low_stock_report()
        for item in report:
            item["stock"] = float(item["stock"])
        return report
    finally:
        db.close()


def get_customer_outstanding_report() -> list[dict]:
    """
    Returns customers with pending Khata balance.
    """
    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        report = service.get_customer_outstanding_report()
        for item in report:
            item["balance"] = float(item["balance"])
        return report
    finally:
        db.close()


def get_inventory_value() -> dict:
    """
    Returns total inventory value.
    """
    db = SessionLocal()
    try:
        service = AnalyticsService(db)
        summary = service.get_inventory_value()
        summary["inventory_value"] = float(summary["inventory_value"])
        return summary
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
        sales = service.get_recent_sales(limit)
        for sale in sales:
            sale["amount"] = float(sale["amount"])
            if sale["created_at"]:
                sale["created_at"] = sale["created_at"].isoformat()
        return sales
    finally:
        db.close()


def generate_sales_report_ppt(
    days: int = 30,
) -> dict:
    """
    Generates a premium business report slide presentation (PPTX).
    Returns a status dict containing the absolute file path.
    """
    db = SessionLocal()
    try:
        from app.services.ppt_service import PPTService

        ppt_service = PPTService(db)
        file_path = ppt_service.generate_sales_report_ppt(days)

        return {
            "status": "success",
            "message": f"Business report generated successfully.",
            "file_path": file_path,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to generate PPTX report: {str(e)}",
        }
    finally:
        db.close()