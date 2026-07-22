from app.database.database import SessionLocal

from app.database.seeders.customer_seeder import seed_customers
from app.database.seeders.inventory_seeder import seed_inventory
from app.database.seeders.preference_seeder import seed_preferences
from app.database.seeders.product_seeder import seed_products


def seed_database():

    db = SessionLocal()

    try:

        seed_products(db)
        seed_customers(db)
        seed_preferences(db)
        seed_inventory(db)

    finally:
        db.close()