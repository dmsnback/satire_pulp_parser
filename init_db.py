import asyncio
import logging

from config import setup_logger
from db_async import engine
from dotenv import load_dotenv
from models import Base, LastSentNews, News  # noqa

load_dotenv()

setup_logger()
logger = logging.getLogger(__name__)


async def init():
    """Создание таблиц в базе"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("...Таблицы созданы...")


asyncio.run(init())
