from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product
import json


class PernaturamSpider(Spider):

    name = 'Pernaturam'
    address = '7000200'
    allowed_domains = ['pernaturam.de']
    start_urls = ['https://www.pernaturam.de']

    def parse(self, response):
        for item in response.css('div.menu-container > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.item-inner > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

        next = response.css('a.pager-next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        for item in response.css('div.selector-items > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)

        i.context['prefix'] = ''
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'div.variant-info.artnr > span.variant-info-value')
        i.add_css('sid', 'div.variant-info.artnr > span.variant-info-value')
        i.add_css('title', 'span.product-title-name')
        i.add_css('size', 'span.selector-title-name')
        i.add_css('price', 'span.price-value')
        i.add_css('time', 'span.available > span.variant-info-value-name')
        
        i.add_css('selector', 'div#breadcrumb > div > div > a > span')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')

        i.add_css('content_1', 'div.product-body')
        i.add_css('content_2', 'section.product-attributes')
        
        i.add_css('content_1_html', 'div.product-body')
        i.add_css('content_2_html', 'section.product-attributes')
        
        for img in response.css('a.gallery-item > img::attr(src)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
