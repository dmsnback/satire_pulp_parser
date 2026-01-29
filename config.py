import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: - |%(levelname)s| %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=1024 * 1024 * 5,
                backupCount=5,
                encoding="utf-8",
            ),
        ],
    )
