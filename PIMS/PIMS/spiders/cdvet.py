from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class CdvetSpider(BaseSpider):

    name = 'cdvet'
    address = '7000010'
    allowed_domains = ['cdvet.de']
    start_urls = ['https://www.cdvet.de']

    def parse(self, response):
        for item in response.css('div.navigation-flyouts a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.card-body > div.product-info > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        pages = self.click(
            url=response.url,
            selector='div.product-detail-configurator-options > div > label',
            delay=10,
            cookies='button#ccAcceptButton'
        )

        for page in pages:
            yield self.parse_product(response=page, parent=page.css('span.product-detail-ordernumber').get())

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'CV'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.product-detail-ordernumber')
        i.add_css('sid', 'span.product-detail-ordernumber')
        i.add_css('ean', 'span.product-detail-ean')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product-detail-name')
        i.add_css('price', 'p.product-detail-price')
        i.add_css('size', 'span.price-unit-content')
        i.add_css('time', 'p.delivery-information')

        i.add_css('selector', 'span.breadcrumb--title')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Produktvorteile')
        i.add_value('title_3', 'Beschreibung')
        i.add_value('title_4', 'Eigenschaften')
        i.add_value('title_5', 'Hersteller')

        i.add_css('content_1', 'div.product-detail-short-description')
        i.add_css('content_2', 'div.mill-product-advantages')
        i.add_css('content_3', 'div.product-detail-description-text')
        i.add_css('content_4', 'div.product-detail-properties')
        i.add_css('content_5', 'div.product-detail-manufacturer')

        i.add_css('content_1_html', 'div.product-detail-short-description')
        i.add_css('content_2_html', 'div.mill-product-advantages')
        i.add_css('content_3_html', 'div.product-detail-description-text')
        i.add_css('content_4_html', 'div.product-detail-properties')
        i.add_css('content_5_html', 'div.product-detail-manufacturer')

        for img in response.css('div.gallery-slider-single-image > img::attr(image)'):
            i.add_value('image_urls', img.get())

        return i.load_item()

