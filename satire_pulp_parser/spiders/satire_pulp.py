import scrapy
from db.db_sync import SessionLocal
from satire_pulp_parser.items import NewsItem
from satire_pulp_parser.spider_storage import is_news_exists


class SatirePulpSpider(scrapy.Spider):
    name = "satire_pulp"
    allowed_domains = ["panorama.pub"]
    start_urls = ["https://panorama.pub"]

    def parse(self, response):
        news_links = response.css("div.shrink-0 li a::attr(href)").getall()
        for link in news_links:
            full_link = response.urljoin(link)
            with SessionLocal() as session:
                if is_news_exists(full_link, session):
                    self.logger.info(f"Новость уже есть: {full_link}")
                    continue

            yield scrapy.Request(url=full_link, callback=self.parse_news)

    def parse_news(self, response):
        title = response.css('h1[itemprop="headline"]::text').get()
        text = response.css("div.entry-contents p::text").get()
        image = response.css('meta[itemprop="image"]::attr(content)').get()
        final_title = title.strip()
        final_text = text.strip()
        if image:
            image = response.urljoin(image).strip()

        else:
            image = None
        item = NewsItem(
            title=final_title, text=final_text, image=image, url=response.url
        )
        yield item
