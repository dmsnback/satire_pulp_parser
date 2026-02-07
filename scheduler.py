import logging
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler
from config import setup_logger

setup_logger()
logger = logging.getLogger(__name__)


def run_spider():
    """Запуск паука"""
    try:
        logger.info("...Запуск парсера...")
        result = subprocess.run(
            ["scrapy", "crawl", "satire_pulp"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            logger.info("...Парсер успешно завершил работу...")
        else:
            logger.error(f"Ошибка при запуске парсера: {result.stderr}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при запуске парсера: {e}")


def run_scheduler():
    scheduler = BlockingScheduler()
    try:
        logger.info("...Планировщик запущен...")
        run_spider()
        scheduler.add_job(run_spider, "interval", minutes=1)
        scheduler.start()
    except Exception as e:
        logger.error(f"Ошибкка в планировщике: {e}")


run_scheduler()
