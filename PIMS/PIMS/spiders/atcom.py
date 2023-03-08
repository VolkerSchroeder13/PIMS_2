from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class AtcomSpider(BaseSpider):

    name = 'atcom'
    address = '7018700B6'
    allowed_domains = ['atcomhorse.de']
    start_urls = ['https://www.atcomhorse.de']

    def parse(self, response):
        for item in response.css('nav.main-navigation-menu > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product-info > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_variation)

    def parse_variation(self, response):
        items = response.css('select.product-configurator-select > option::attr(value)')

        for item in items:
            url = self.get_page(
                url=response.url, 
                select='select.product-configurator-select', 
                option=item.get()
            )
            yield Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'AT'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.product-detail-ordernumber')

        yield i.load_item()