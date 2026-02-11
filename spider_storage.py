import logging

from models import News
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


def is_news_exists(url: str, session):
    """Проверка новости в базе по URL"""
    try:
        news = session.query(News).filter(News.url == url)
        return news.first() is not None
    except SQLAlchemyError as e:
        logger.error(f"Ошибка проверки новости в базе: {e}")
        raise


def save_news(url: str, title: str, image: str, text: str, session):
    """Созранение новости в базе."""
    try:
        news = News(url=url, title=title, image=image, text=text)
        session.add(news)
        session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка сохранения новости в бд: {e}")
        raise
