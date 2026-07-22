from sqlalchemy.orm import Session

from app.models.customer import Customer
from sqlalchemy import select


CUSTOMERS = [
    {
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "email": "rahul@example.com",
        "address": "Kochi",
    },
    {
        "name": "Anjali Nair",
        "phone": "9876543211",
        "email": "anjali@example.com",
        "address": "Thrissur",
    },
    {
        "name": "Walk-in Customer",
        "phone": None,
        "email": None,
        "address": None,
    },
]


def seed_customers(db: Session) -> None:

    for customer in CUSTOMERS:


        exists = db.scalar(
            select(Customer).where(Customer.name == customer["name"])
        )
        if exists:
            continue

        db.add(Customer(**customer))

    db.commit()

    print("Customers seeded.")