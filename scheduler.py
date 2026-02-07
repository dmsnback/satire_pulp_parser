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


def run_bot():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.job_queue.run_repeating(auto_send_news, interval=10, first=10)
    app.add_handler(CommandHandler("start", menu))
    app.add_handler(CommandHandler("show_news", show_news_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    asyncio.get_event_loop().run_until_complete(set_commands(app))
    logger.info("... Бот запущен ...")
    app.run_polling()
    logger.info("... Бот остановлен ...")


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
