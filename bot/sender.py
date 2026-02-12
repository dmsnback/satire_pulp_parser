import logging

from config import setup_logger
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

load_dotenv()

setup_logger()
logger = logging.getLogger(__name__)


MAX_CAPTION_LENGTH = 1024


def format_message(title, text):
    message = f"*{title}*\n\n{text}\n"
    if len(message) > MAX_CAPTION_LENGTH:
        message = f"*{title}*\n\n{text[:MAX_CAPTION_LENGTH]} ...✂️\n"
    return message


async def send_news(
    chat_id: int, context: ContextTypes.DEFAULT_TYPE, title, image, text, url
):
    message = format_message(title, text)
    keyboard = [
        [InlineKeyboardButton("Читать полную версию на сайте", url=url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if image:
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=image,
                caption=message,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
            logger.info("Новость отправлена с картинкой")
            return
        except Exception as e:
            logger.error(
                f"Не удалось отправить фото по ссылке, ошибка: {e}",
            )
    try:
        await context.bot.send_message(
            chat_id, message, parse_mode="Markdown", reply_markup=reply_markup
        )
        logger.info(f"Новость '{title[:25]}' отправлена без картинки")
    except Exception as e:
        logger.error(
            f"Не удалось отправить сообщение с новостью '{title[:25]}', ошибка: {e}"
        )
