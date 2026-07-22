from decimal import Decimal

from app.database.database import SessionLocal

from app.schemas.inventory import (
    InventoryTransactionCreate,
)

from app.services.inventory_service import (
    InventoryService,
)

from app.utils.serializers import (
    serialize_inventory_transaction,
    serialize_inventory_transactions,
)


def record_purchase(
    transaction: InventoryTransactionCreate,
) -> dict:
    """
    Records stock received into inventory.
    """

    db = SessionLocal()

    try:

        service = InventoryService(db)

        inventory = service.record_purchase(
            transaction
        )

        service.commit()

        return serialize_inventory_transaction(
            inventory
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()

def record_sale(
    transaction: InventoryTransactionCreate,
) -> dict:
    """
    Records stock removed after a sale.
    """

    db = SessionLocal()

    try:

        service = InventoryService(db)

        inventory = service.record_sale(
            transaction
        )

        service.commit()

        return serialize_inventory_transaction(
            inventory
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()

def get_current_stock(
    product_id: int,
) -> dict:
    """
    Returns current stock for a product.
    """

    db = SessionLocal()

    try:

        service = InventoryService(db)

        stock = service.get_current_stock(
            product_id
        )

        return {
            "product_id": product_id,
            "stock": float(stock),
        }

    finally:

        db.close()

def get_stock_history(
    product_id: int,
) -> list[dict]:
    """
    Returns inventory history for a product.
    """

    db = SessionLocal()

    try:

        service = InventoryService(db)

        history = service.get_stock_history(
            product_id
        )

        return serialize_inventory_transactions(
            history
        )

    finally:

        db.close()

def get_low_stock_products():
    """
    Returns products below the configured stock threshold.
    """

    db = SessionLocal()

    try:

        service = InventoryService(db)

        products = service.get_low_stock_products()

        return [
            {
                "product": item["product"].name,
                "sku": item["product"].sku,
                "stock": float(item["stock"]),
            }
            for item in products
        ]

    finally:

        db.close()

def adjust_stock(
    product_id: int,
    quantity: Decimal,
) -> dict:
    """
    Adjusts stock to a target quantity.
    """

    db = SessionLocal()

    try:

        service = InventoryService(db)

        transaction = service.adjust_stock(
            product_id,
            quantity,
        )

        service.commit()

        return serialize_inventory_transaction(
            transaction
        )

    except Exception:

        service.rollback()
        raise

    finally:

        db.close()