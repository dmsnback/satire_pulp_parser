import logging
import os

from config import setup_logger
from dotenv import load_dotenv
from storage import get_news_after_id
from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

load_dotenv()

setup_logger()
logger = logging.getLogger(__name__)


MAX_CAPTION_LENGTH = 1024
LAST_ID_FILE = "last_id.txt"


def format_message(title, text):
    message = f"*{title}*\n\n{text}\n"
    if len(message) > MAX_CAPTION_LENGTH:
        message = f"*{title}*\n\n{text[:MAX_CAPTION_LENGTH]} ...✂️\n"
    return message


def get_last_sent_id():
    """Получение id последней новости"""
    if not os.path.exists(LAST_ID_FILE):
        return 0
    with open(LAST_ID_FILE, "r") as f:
        return int(f.read())


def save_last_sent_id(last_id):
    """Сохранение id последней новости"""
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(last_id))


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


async def auto_send_news(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    last_id = get_last_sent_id()
    news_list = get_news_after_id(last_id)
    if not news_list:
        return
    for news_id, title, image, text, url in news_list:
        try:
            await send_news(chat_id, context, title, image, text, url)
            save_last_sent_id(news_id)
        except Exception as e:
            logger.error(f"Ошибка при автоматической отправке новости: {e}")


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📰 Показать новости", callback_data="send_news"
            )
        ],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выберите действие:", reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"callback_query не удалось ответить: {e}")
    if query.data == "send_news":

        last_id = get_last_sent_id()
        news_list = get_news_after_id(last_id)
        if not news_list:
            await query.message.reply_text("Новостей пока нет 🙁")
            logger.info("Новостей нет")
            return
        for news_id, title, image, text, url in news_list:
            try:
                await send_news(
                    query.message.chat_id, context, title, image, text, url
                )
                save_last_sent_id(news_id)
            except Exception as e:
                logger.error(
                    f"Ошибка при отправке новости '{title[:25]}': {e}"
                )
    elif query.data == "help":
        help_text = "Нажмите 📰 'Показать blaновости', чтобы получить новости."
        await query.message.reply_text(help_text)


async def show_news_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    last_id = get_last_sent_id()
    news_list = get_news_after_id(last_id)
    if not news_list:
        await update.message.reply_text("Новостей пока нет 🙁")
        logger.info("Новостей нет")
        return
    try:
        for news_id, title, image, text, url in news_list:
            await send_news(
                update.message.chat_id, context, title, image, text, url
            )
            save_last_sent_id(news_id)
    except Exception as e:
        logger.error(f"Ошибка при отправке новости '{title[:25]}': {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Нажмите 📰 'Показать новости', чтобы получить новости."
    await update.message.reply_text(help_text)


async def set_commands(app):
    commands = [
        BotCommand("start", "Главное меню"),
        BotCommand("show_news", "Показать новости"),
        BotCommand("help", "Помощь"),
    ]
    await app.bot.set_my_commands(commands)
