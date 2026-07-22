from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import InventoryTransaction
from app.models.products import Product
from app.models.enums import InventoryTransactionType


def seed_inventory(db: Session):
    """
    Creates an initial purchase transaction
    for every seeded product.
    """

    products = db.scalars(
        select(Product)
    ).all()

    if not products:
        print(
            "No products found. Skipping inventory seeding."
        )
        return

    for product in products:

        exists = db.scalar(
            select(InventoryTransaction).where(
                InventoryTransaction.product_id
                == product.id
            )
        )

        if exists:
            continue

        db.add(
            InventoryTransaction(
                product_id=product.id,
                transaction_type=InventoryTransactionType.PURCHASE,
                quantity=100,
                reference="Initial Stock",
                remarks="Database seed",
            )
        )

    db.commit()

    print("Inventory seeded.")