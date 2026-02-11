import logging

from bot_storage import (
    get_all_users,
    get_last_sent_id,
    get_news_after_id,
    save_last_sent_news_id,
)
from config import setup_logger
from db_async import AsyncSessionLocal
from dotenv import load_dotenv
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


async def auto_send_news(context: ContextTypes.DEFAULT_TYPE):
    async with AsyncSessionLocal() as session:
        users = await get_all_users(session)
        if not users:
            return
        for chat_id in users:
            last_id = await get_last_sent_id(chat_id, session)
            news_list = await get_news_after_id(last_id, session)
            if not news_list:
                continue
            for news in news_list:
                try:
                    await send_news(
                        chat_id,
                        context,
                        news.title,
                        news.image,
                        news.text,
                        news.url,
                    )
                    await save_last_sent_news_id(chat_id, news.id, session)
                except Exception as e:
                    logger.error(
                        f"Ошибка при автоматической отправке новости: {e}"
                    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = update.message.chat_id
    welcome_text = (
        "Привеет\!\n"
        "Я бот, который присылает сатирические новости с сайта [*Панорама*](https://panorama.pub)\.\n\n"
        "Нажмите 📰 '*Показать новости*', чтобы получить новости\.\n\n"
        "Если на сайте появится новая новость \- я пришлю её\."
    )
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
        welcome_text, reply_markup=reply_markup, parse_mode="MarkdownV2"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except Exception as e:
        logger.warning(f"callback_query не удалось ответить: {e}")
    if query.data == "send_news":
        chat_id = query.message.chat_id
        async with AsyncSessionLocal() as session:
            last_id = await get_last_sent_id(chat_id, session)
            news_list = await get_news_after_id(last_id, session)
            if not news_list:
                await query.message.reply_text("Новых новостей пока нет 🙁")
                logger.info("Новых новостей нет")
                return
            for news in news_list:
                try:
                    await send_news(
                        chat_id,
                        context,
                        news.title,
                        news.image,
                        news.text,
                        news.url,
                    )
                    await save_last_sent_news_id(chat_id, news.id, session)
                except Exception as e:
                    logger.error(
                        f"Ошибка при отправке новости '{news.title[:25]}': {e}"
                    )
    elif query.data == "help":
        help_text = "Нажмите 📰 'Показать новости', чтобы получить новости."
        await query.message.reply_text(help_text)


async def show_news_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.message.chat_id
    async with AsyncSessionLocal() as session:
        last_id = await get_last_sent_id(chat_id, session)
        news_list = await get_news_after_id(last_id, session)
        if not news_list:
            await update.message.reply_text("Новостей пока нет 🙁")
            logger.info("Новостей нет")
            return
        try:
            for news in news_list:
                await send_news(
                    chat_id,
                    context,
                    news.title,
                    news.image,
                    news.text,
                    news.url,
                )
                await save_last_sent_news_id(chat_id, news.id, session)
        except Exception as e:
            logger.error(
                f"Ошибка при отправке новости '{news.title[:25]}': {e}"
            )


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
