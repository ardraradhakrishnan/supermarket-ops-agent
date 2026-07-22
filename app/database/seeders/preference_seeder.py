from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.preference import Preference


PREFERENCES = [
    {
        "key": "store_name",
        "value": "BigMantra Supermarket",
        "description": "Store Name",
    },
    {
        "key": "currency",
        "value": "INR",
        "description": "Currency",
    },
    {
        "key": "low_stock_threshold",
        "value": "10",
        "description": "Low Stock Alert",
    },
    {
        "key": "invoice_prefix",
        "value": "INV",
        "description": "Invoice Prefix",
    },
]


def seed_preferences(db: Session):
    """
    Seeds application preferences.
    """

    for pref in PREFERENCES:

        exists = db.scalar(
            select(Preference).where(
                Preference.key == pref["key"]
            )
        )

        if exists:
            continue

        db.add(Preference(**pref))

    db.commit()

    print("Preferences seeded.")