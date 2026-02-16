import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    text = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
