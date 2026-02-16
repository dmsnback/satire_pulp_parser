import logging

from db.db_sync import SessionLocal
from satire_pulp_parser.items import NewsItem
from satire_pulp_parser.spider_storage import save_news

logger = logging.getLogger(__name__)


class SaveNewsPipeline:
    def process_item(self, item: NewsItem, spider):
        try:
            with SessionLocal() as session:
                save_news(
                    url=item["url"],
                    title=item["title"],
                    image=item["image"],
                    text=item["text"],
                    session=session,
                )
                logger.info("...Новость сохранена...")
        except Exception as e:
            logger.error(f"Ошибка при сохранении новости: {e}")
        return item
