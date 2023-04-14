from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class EquanisSpider(Spider):

    name = 'equanis'
    address = '7028800'
    allowed_domains = ['equanis.de']
    start_urls = ['https://www.equanis.de']

    def parse(self, response):
        item = response.css('#menu-item-6481 > a::attr(href)')
        yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.box-image > div.image-zoom > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'EQ'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.sku_wrapper > span.sku')
        i.add_css('sid', 'span.sku_wrapper > span.sku')
        i.add_value('parent', None)
        i.add_css('title', 'h1.product-title')
        i.add_css('price', 'div.price-wrapper > p > span > bdi')
        i.add_css('size', 'tr.woocommerce-product-attributes-item--weight > td.woocommerce-product-attributes-item__value')
        i.add_css('time', 'p.delivery-time-info')
        
        i.add_css('selector', 'span.posted_in > a')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Zusätzliche Informationen')
        
        i.add_css('content_1', 'div.product-short-description')
        i.add_css('content_2', 'div.woocommerce-Tabs-panel--description')
        i.add_css('content_3', 'div.woocommerce-Tabs-panel--additional_information')
        
        i.add_css('content_1_html', 'div.product-short-description')
        i.add_css('content_2_html', 'div.woocommerce-Tabs-panel--description')
        i.add_css('content_3_html', 'div.woocommerce-Tabs-panel--additional_information')
        
        for img in response.css('div.woocommerce-product-gallery__image > a::attr(href)'):
            i.add_value('image_urls', img.get())
        
        yield i.load_item()
