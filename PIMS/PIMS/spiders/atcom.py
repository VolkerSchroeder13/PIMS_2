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
            result = self.select(
                url=response.url, 
                select='div.product-detail-configurator-options > select', 
                option=item.get(),
                delay=5
            )
            yield self.parse_product(response=result, parent=result.css('span.product-detail-ordernumber').get())
            
    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'AT'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.product-detail-ordernumber')
        i.add_css('sid', 'span.product-detail-ordernumber')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product-detail-name')
        i.add_css('price', 'p.product-detail-price')
        i.add_css('size', 'select.product-configurator-select > option[selected]')
        i.add_css('time', 'p.delivery-information')

        i.add_css('selector', 'ol.breadcrumb >  li > a > span')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Fütterungsempfehlung')
        i.add_value('title_4', 'Zusammensetzung')

        i.add_css('content_1', 'div.product-detail-description-short-content')
        i.add_css('content_2', 'div[id="description-tab-pane"]')
        i.add_css('content_3', 'div[id="feeding-recommendation-tab-pane"]')
        i.add_css('content_4', 'div[id="product-detail-tab-pane"]')
   
        i.add_css('content_1_html', 'div.product-detail-description-short-content')
        i.add_css('content_2_html', 'div[id="description-tab-pane"]')
        i.add_css('content_3_html', 'div[id="feeding-recommendation-tab-pane"]')
        i.add_css('content_4_html', 'div[id="product-detail-tab-pane"]')

        for img in response.css('div.gallery-slider-item-container > div > img::attr(data-src)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        return i.load_item()