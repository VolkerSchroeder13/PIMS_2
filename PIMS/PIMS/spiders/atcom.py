from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class AtcomSpider(BaseSpider):

    name = 'atcom'
    address = '7018700B6'
    allowed_domains = ['atcomhorse.de']
    start_urls = ['https://www.atcomhorse.de/p/atcom-senior-vital/161266']

    def parse(self, response):
        items = response.css('select.product-configurator-select > option::attr(value)').getall()

        for item in items:
            print(item + '\n')
            result = self.next(
                url=response.url, 
                select='div.product-detail-configurator-options > select', 
                option=item
            )
            yield self.parse_product(response=result)
            

    def parse_product(self, response):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'AT'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.product-detail-ordernumber')
        i.add_css('title', 'h1.product-detail-name')
        i.add_css('size', 'select.product-configurator-select > option[selected]')

        return i.load_item()