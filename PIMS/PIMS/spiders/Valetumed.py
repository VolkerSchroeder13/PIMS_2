from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class ValetumedSpider(Spider):

    name = 'Valetumed'
    address = '7022100'
    allowed_domains = ['valetumed.de']
    start_urls = ['https://www.valetumed.de']

    def parse(self, response):
        for item in response.css('ul.menu-hauptmenue > li > div > div > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product-wrapper > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        size = str(response.css('p.product-units')) + str(response.css('span.unit'))

        i.context['prefix'] = 'ML'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.sku')
        i.add_css('sid', 'span.sku')
        i.add_css('title', 'h1.product_title')
        i.add_css('price', 'span.woocommerce-Price-amount > bdi')
        i.add_value('size', size)
        i.add_css('time', 'p.delivery-time-info')
        
        i.add_css('selector', 'nav.woocommerce-breadcrumb > a')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Fütterungshinweise und Zutaten')

        i.add_css('content_1', 'div.woocommerce-product-details__short-description')
        i.add_css('content_2', 'div.woocommerce-Tabs-panel--description')
        i.add_css('content_3', 'div.woocommerce-Tabs-panel--fuetterungshinweise-und-zutaten')
        
        i.add_css('content_1_html', 'div.woocommerce-product-details__short-description')
        i.add_css('content_2_html', 'div.woocommerce-Tabs-panel--description')
        i.add_css('content_3_html', 'div.woocommerce-Tabs-panel--fuetterungshinweise-und-zutaten')
        
        for img in response.css('div.owl-stage > div.owl-item > div > figure > a::attr(href)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
