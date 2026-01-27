import scrapy
from storage import init_db, is_news_exists, save_news


class SatirePulpSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_db()

    name = "satire_pulp"
    allowed_domains = ["panorama.pub"]
    start_urls = ["https://panorama.pub"]

    def parse(self, response):
        news_links = response.css("div.shrink-0 li a::attr(href)").getall()
        for link in news_links:
            full_link = response.urljoin(link)
            if is_news_exists(full_link):
                self.logger.info(f"Новость уже есть: {full_link}")
                continue

            yield scrapy.Request(url=full_link, callback=self.parse_news)

    def parse_news(self, response):
        title = response.css('h1[itemprop="headline"]::text').get()
        text = response.css("div.entry-contents p::text").getall()
        image = response.css('meta[itemprop="image"]::attr(content)').get()
        final_text = " ".join(text).strip()
        save_news(response.url, title)
        yield {
            "title": title,
            "text": final_text,
            "image": image,
            "url": response.url,
        }
