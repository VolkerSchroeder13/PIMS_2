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
        for item in response.css('div.product-detail-configurator-options > select > option::attr(value)'):
            result = self.variation(
                url=response.url, 
                select='div.product-detail-configurator-options > select', 
                option=item.get(),
                delay=3
            )
            yield self.parse_product(response=result)
            
    def parse_product(self, response):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'AT'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.product-detail-ordernumber')
        i.add_css('title', 'h1.product-detail-name')
        i.add_css('price', 'p.product-detail-price')
        i.add_css('size', 'select.product-configurator-select > option[selected]')
        i.add_css('time', 'p.delivery-information')

        i.add_css('selector', 'ol.breadcrumb >  li > a > span')

        i.add_css('short_description', 'div.product-detail-description-short-content')
        i.add_css('description', 'div[id="description-tab-pane"]')
        i.add_css('recommendation', 'div[id="feeding-recommendation-tab-pane"]')
        i.add_css('composition', 'div[id="product-detail-tab-pane"]')
        
        i.add_value('recommendation_title', 'Fütterungsempfehlung')
        i.add_value('composition_title', 'Zusammensetzung')
   
        i.add_css('short_description_html', 'div.product-detail-description-short-content')
        i.add_css('description_html', 'div[id="description-tab-pane"]')
        i.add_css('recommendation_html', 'div[id="feeding-recommendation-tab-pane"]')
        i.add_css('composition_html', 'div[id="product-detail-tab-pane"]')

        return i.load_item()