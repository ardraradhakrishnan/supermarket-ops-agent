import os
import logging
from app.core.config import get_settings

def setup_logging(log_filename: str = "supermarket_bot.log") -> str:
    settings = get_settings()
    log_dir = os.path.abspath("logs")
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_filename)
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.handlers:
        root_logger.handlers.clear()

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)

    logger = logging.getLogger("app.core.logger")
    logger.info(f"Logging initialized. Log file at: {log_path}")
    return log_path
