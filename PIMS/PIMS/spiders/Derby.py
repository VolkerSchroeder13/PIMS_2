from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class DerbySpider(BaseSpider):

    name = 'Derby'
    address = '7000017'
    allowed_domains = ['derby.de']
    start_urls = ['https://www.derby.de']

    def parse(self, response):
        for item in response.css('div.flyout__default > div > div > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.card-body > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        pages = self.click(
            url=response.url, 
            selector='div.product-detail-configurator-option > label',
            delay=10,
            cookies='span.js-cookie-accept-all-button'
        )

        for page in pages:
            yield self.parse_product(
                response=page, 
                parent=response.css('div.properties > div:nth-child(2) > div.values').get()
            )

        yield self.parse_product(response=self.page(response.url), parent=None)

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'EO'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'div.properties > div:nth-child(2) > div.values')
        i.add_css('sid', 'div.properties > div:nth-child(2) > div.values')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product-detail-name')
        i.add_css('price', 'p.product-detail-price')
        i.add_value('size', response.css('span.price-unit-content').get().replace('.',','))
        
        i.add_css('selector', 'ol.breadcrumb > li > a > span')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Fütterungsempfehlung')
        
        i.add_css('content_1', 'div.mb-4')
        i.add_css('content_2', 'div.product-detail-description')
        i.add_css('content_3', 'div.product-detail-custom-field')

        i.add_css('content_1_html', 'div.mb-4')
        i.add_css('content_2_html', 'div.product-detail-description')
        i.add_css('content_3_html', 'div.product-detail-custom-field')

        for img in response.css('div.gallery-slider-item > img::attr(content)'):
            i.add_value('image_urls', img.get())
        
        return i.load_item()
