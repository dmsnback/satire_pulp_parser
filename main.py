import asyncio
import logging
import os

from bot import (
    auto_send_news,
    button_handler,
    help_command,
    menu,
    set_commands,
    show_news_command,
)
from config import setup_logger
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
)

load_dotenv()

setup_logger()
logger = logging.getLogger(__name__)


def main():
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


if __name__ == "__main__":
    main()
