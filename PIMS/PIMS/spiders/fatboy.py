from PIMS.PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class FatboySpider(BaseSpider):

    name = 'fatboy'
    address = '7022600'
    allowed_domains = ['fatboy.com']
    start_urls = ['https://www.fatboy.com/de-de']

    def parse(self, response):
        response = self.page(response.url)
        
        for category in response.css('nav.navigation--desktop > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(category.get()), callback=self.parse_category)

    def parse_category(self, response):
        response = self.page(response.url)
        
        for product in response.css('ul.grid > li > div > a::attr(href)'):
            yield Request(url=response.urljoin(product.get()), callback=self.parse_variation)

        next = response.css('ul.pagination > li:nth-child(3) > a::attr(href)')
        if next is not None:    
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        response = self.page(response.url)
        
        for product in response.css('select.product-form__variants > option::attr(value)'):
            yield Request(url=(response.url+'/?variant='+product.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)

        i.context['prefix'] = 'FB'

        yield i.load_item()
