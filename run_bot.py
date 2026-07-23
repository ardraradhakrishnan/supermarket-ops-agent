import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

import logging
from app.core.logger import setup_logging
from app.database.database import init_db
from app.database.seed import seed_database
from app.bot.telegram_bot import main as start_bot

def main():
    log_file = setup_logging("supermarket_bot.log")
    logger = logging.getLogger("run_bot")
    
    logger.info("--------------------------------------------")
    logger.info("Starting Supermarket Operational Bot Startup...")
    logger.info("--------------------------------------------")
    
    logger.info("Initializing Database...")
    init_db()
    logger.info("Database Initialized.")
    
    logger.info("Seeding Database...")
    seed_database()
    logger.info("Database Seed Complete.")
    
    logger.info(f"Starting Bot Service (logging progress to {log_file})...")
    start_bot()

if __name__ == "__main__":
    main()
