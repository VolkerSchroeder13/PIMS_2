from PIMS.items import Product
from scrapy import Spider, Request
from scrapy.loader import ItemLoader


class AtcomSpider(Spider):

    name = 'atcom'
    allowed_domains = ['atcomhorse.de']
    start_urls = ['https://www.atcomhorse.de']

    def parse(self, response):
        pass