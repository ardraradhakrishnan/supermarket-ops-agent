import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from app.database.database import init_db
from app.database.seed import seed_database
from app.bot.telegram_bot import main as start_bot

def main():
    print("--------------------------------------------")
    print("Starting Supermarket Operational Bot Startup...")
    print("--------------------------------------------")
    
    print("Initializing Database...")
    init_db()
    print("Database Initialized.")
    
    print("Seeding Database...")
    seed_database()
    print("Database Seed Complete.")
    
    print("Starting Bot Service...")
    start_bot()

if __name__ == "__main__":
    main()
