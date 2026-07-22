from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.products import Product
from app.models.enums import Unit


PRODUCTS = [
    {
        "sku": "SKU001",
        "name": "Basmati Rice",
        "description": "Premium long grain rice",
        "unit_price": Decimal("65.00"),
        "gst_rate": 5,
        "unit": Unit.KG,
    },
    {
        "sku": "SKU002",
        "name": "Milk",
        "description": "Fresh toned milk",
        "unit_price": Decimal("32.00"),
        "gst_rate": 5,
        "unit": Unit.LITRE,
    },
    {
        "sku": "SKU003",
        "name": "Sugar",
        "description": "Refined white sugar",
        "unit_price": Decimal("45.00"),
        "gst_rate": 5,
        "unit": Unit.KG,
    },
    {
        "sku": "SKU004",
        "name": "Maggi Noodles",
        "description": "Instant noodles",
        "unit_price": Decimal("14.00"),
        "gst_rate": 12,
        "unit": Unit.PACK,
    },
    {
        "sku": "SKU005",
        "name": "Sunflower Oil",
        "description": "Refined cooking oil",
        "unit_price": Decimal("180.00"),
        "gst_rate": 5,
        "unit": Unit.LITRE,
    },
    {
        "sku": "SKU006",
        "name": "Tea Powder",
        "description": "Premium tea",
        "unit_price": Decimal("220.00"),
        "gst_rate": 5,
        "unit": Unit.KG,
    },
    {
        "sku": "SKU007",
        "name": "Coffee Powder",
        "description": "Instant coffee",
        "unit_price": Decimal("450.00"),
        "gst_rate": 5,
        "unit": Unit.KG,
    },
    {
        "sku": "SKU008",
        "name": "Bread",
        "description": "Whole wheat bread",
        "unit_price": Decimal("40.00"),
        "gst_rate": 5,
        "unit": Unit.PACK,
    },
    {
        "sku": "SKU009",
        "name": "Eggs",
        "description": "Farm fresh eggs",
        "unit_price": Decimal("7.00"),
        "gst_rate": 0,
        "unit": Unit.PIECE,
    },
    {
        "sku": "SKU010",
        "name": "Bath Soap",
        "description": "Herbal soap",
        "unit_price": Decimal("35.00"),
        "gst_rate": 18,
        "unit": Unit.PIECE,
    },
]


def seed_products(db: Session) -> None:
    """
    Seed initial products.
    """

    for product in PRODUCTS:
        

        exists = db.scalar(
            select(Product).where(Product.sku == product["sku"])
        )

        if exists:
            continue

        db.add(Product(**product))

    db.commit()

    print("Products seeded.")