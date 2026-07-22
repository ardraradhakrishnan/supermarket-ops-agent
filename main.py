import app.models

from app.database.database import init_db
from app.database.seed import seed_database


def main():
    print("Initializing database...")

    init_db()

    print("Database initialized successfully.")

    print("Seeding database...")
    seed_database()

    print("Supermarket Ops Agent started successfully.")



if __name__ == "__main__":
    main()