from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
from time import sleep
import json


class VetripharmSpider(BaseSpider):
    custom_settings = {
        # "DOWNLOAD_DELAY": "1.5",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    name = 'Vetripharm'
    address = '7017900'
    allowed_domains = ['vetripharm.de']
    start_urls = ['https://vetripharm.de/de/']

    visited_products = []
    visited_variations = []

    def search_json_item(self, contained_str, page, script_selector):
        json_item = None
        for script in page.css(script_selector).getall():
            if contained_str in script:
                json_item = json.loads(script)
        return json_item

    def parse(self, response):
        for href in response.css('li[title="produkte"] ul.uk-nav li a::attr(href)').getall():
            if(href == '#'):
                continue
            yield Request(url=response.urljoin(href), callback=self.parse_category)

    def parse_category(self, response):
        pass

    def parse_variation(self, response):
        pass

    def parse_product(self, response, parent, variation):
        pass
