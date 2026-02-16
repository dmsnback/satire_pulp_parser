import logging

from db.models import LastSentNews, News
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def get_news_after_id(last_id: int, session: AsyncSession, n=10):
    """
    Получение новостей если если id новости меньше чем last_id отправленной новости,
        либо получение 10 последних новостей если last_id = 0
    """
    try:
        if last_id == 0:
            news = await session.execute(
                select(News)
                .where(News.id > last_id)
                .order_by(News.id.desc())
                .limit(n)
            )
            return news.scalars().all()[::-1]
        else:
            news = await session.execute(
                select(News).where(News.id > last_id).order_by(News.id.asc())
            )
            return news.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении списка новостей: {e}")
        raise


async def get_last_sent_id(chat_id: int, session: AsyncSession):
    """Получение last_id последней отправленной новости"""
    try:
        last_sent = await session.execute(
            select(LastSentNews).where(LastSentNews.chat_id == chat_id)
        )
        last_sent_id = last_sent.scalar_one_or_none()
        if last_sent_id:
            return last_sent_id.last_news_id
        else:
            return 0
    except SQLAlchemyError as e:
        logger.error(
            f"Ошибка при получении id последней отправленной новости: {e}"
        )


async def save_last_sent_news_id(
    chat_id: int, last_id: int, session: AsyncSession
):
    """Сохранение last_id последней отправленной новости"""
    try:
        last_sent = await session.execute(
            select(LastSentNews).where(LastSentNews.chat_id == chat_id)
        )
        last_sent = last_sent.scalar_one_or_none()
        if last_sent:
            last_sent.last_news_id = last_id
        else:
            last_sent = LastSentNews(chat_id=chat_id, last_news_id=last_id)
            session.add(last_sent)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Ошибка при сохранении last_news_id: {e}")
        raise


async def get_all_users(session: AsyncSession):
    """Получение id юзера"""
    try:
        users = await session.execute(select(LastSentNews.chat_id))
        return users.scalars().all()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка получения chat_id пользователей: {e}")
