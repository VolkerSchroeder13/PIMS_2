from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product
import json


class SpeedSpider(Spider):

    name = 'Speed'
    address = '7022100'
    allowed_domains = ['www.speed-horse.care']
    start_urls = ['https://www.speed-horse.care']

    def parse(self, response):
        for item in response.css('ul.menu-hauptmenue-1 > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product-wrapper > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        data = json.loads(response.css('script[type="application/ld+json"]::text').get())

        i.context['prefix'] = 'ML'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_value('id', data['sku'])
        i.add_value('sid', data['sku'])
        i.add_css('title', 'h1.product_title')
        i.add_css('size', 'td.woocommerce-product-attributes-item__value')
        i.add_css('time', 'p.delivery-time-info')
        
        i.add_css('selector', 'nav.woocommerce-breadcrumb > a')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Zutaten')
        i.add_value('title_4', 'Fütterungsempfehlung')

        i.add_css('content_1', 'div.woocommerce-product-details__short-description')
        i.add_css('content_2', 'div.woocommerce-Tabs-panel--description')
        i.add_css('content_3', 'div.woocommerce-Tabs-panel--zutaten')
        i.add_css('content_4', 'div.woocommerce-Tabs-panel--fuetterungsempfehlung')
        
        i.add_css('content_1_html', 'div.woocommerce-product-details__short-description')
        i.add_css('content_2_html', 'div.woocommerce-Tabs-panel--description')
        i.add_css('content_3_html', 'div.woocommerce-Tabs-panel--zutaten')
        i.add_css('content_4_html', 'div.woocommerce-Tabs-panel--fuetterungsempfehlung')
        
        for img in response.css('div.owl-stage > div.owl-item > div > figure > a::attr(href)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
