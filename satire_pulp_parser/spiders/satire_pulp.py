import scrapy


class SatirePulpSpider(scrapy.Spider):
    name = "satire_pulp"
    allowed_domains = ["panorama.pub"]
    start_urls = ["https://panorama.pub"]

    def parse(self, response):
        self.logger.info("Главная страница Панорамы")
        news_links = response.css("div.shrink-0 li a::attr(href)").getall()
        for link in news_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(url=full_link, callback=self.parse_news)

    def parse_news(self, response):
        title = response.css('h1[itemprop="headline"]::text').get()
        text = response.css("div.entry-contents p::text").getall()
        image = response.css('meta[itemprop="image"]::attr(content)').get()
        final_text = " ".join(text).strip()
        self.logger.info(f"ЗАГОЛОВОК: {title}")
        self.logger.info(f"ТЕКСТ: {final_text}")
        self.logger.info(f"КАРТИНКА: {image}")
