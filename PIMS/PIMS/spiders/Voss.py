from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
from time import sleep
import json


class VossSpider(BaseSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": "0",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    name = 'Voss'
    address = '7024400'
    allowed_domains = ['weidezaun.info']
    start_urls = ['https://www.weidezaun.info/']

    def search_json_item(self, contained_str, page, script_selector):
        json_item = None
        for script in page.css(script_selector).getall():
            if contained_str in script:
                json_item = json.loads(script)
        return json_item

    def parse(self, response):
        # ul.nav > li ul ul li a
        for href in response.css('ul.nav > li ul ul li a::attr(href)').getall():
            if(href == '#'):
                continue
            yield Request(url=response.urljoin(href), callback=self.parse_category)

    def parse_category(self, response):
        # ul.pagination li[data-id="Page"] a
        for href in response.css('ul.pagination li[data-id="Page"] a::attr(href)').getall():
            if(href == '#'):
                continue
            yield Request(url=response.urljoin(href), callback=self.parse_page)

    def parse_page(self, response):
        # div.classic div[class*="title"] a
        for href in response.css('div.classic div[class*="title"] a::attr(href)').getall():
            if(href == '#'):
                continue
            yield Request(url=response.urljoin(href), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), selector=response)

        # General info
        i.context['prefix'] = ''
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span[itemprop=sku]')
        i.add_css('sid', 'span[itemprop=sku]')
        # i.add_value('parent', parent)
        # i.add_value('size', selected_quantity)
        i.add_css('title', 'h1[itemprop="name"]')
        i.add_css('price', 'div.price span[itemprop="price"]')
        i.add_css('time', 'span.deliverytime')

        i.add_css('selector', 'span[class*="breadcrumb"]')

        # Descriptions
        i.add_value('title_1', 'Beschreibung')
        i.add_value('title_2', 'Auf einen Blick')
        i.add_value('title_3', 'Details')
        i.add_value('title_4', 'Lieferumfang')

        i.add_css('content_1', 'div.beschreibungBox div.contentBox-content')
        i.add_css('content_2', 'div.aufeinblickBox div.contentBox-content')
        i.add_css('content_3', 'div.detailsBox div.contentBox-content')
        i.add_css('content_4', 'div.lieferumfangBox div.contentBox-content')

        i.add_css('content_1_html', 'div.beschreibungBox div.contentBox-content')
        i.add_css('content_2_html', 'div.aufeinblickBox div.contentBox-content')
        i.add_css('content_3_html', 'div.detailsBox div.contentBox-content')
        i.add_css('content_4_html', 'div.lieferumfangBox div.contentBox-content')

        # Product images
        i.add_css('image_urls', 'div.articlewrapper picture img::attr(src)')

        return i.load_item()
