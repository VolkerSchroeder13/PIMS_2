from scrapy.loader import ItemLoader
from scrapy import Request, Spider
from PIMS.items import Product


class MairolSpider(Spider):

    name = 'Mairol'
    address = '7025200'
    allowed_domains = ['mairol-shop.de']
    start_urls = ['https://www.mairol-shop.de/Unsere-Duenger']

    def parse(self, response):
        for item in response.css('ul.nav > li > div > ul > li > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_category)

        for item in response.css('#crd-cllps-124 > div > ul > li:nth-child(2) > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.productbox-inner > div > div > div > div > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'BA'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'li.product-sku > span')
        i.add_css('sid', 'li.product-sku > span')
        i.add_value('parent', None)
        i.add_css('title', 'h1.product-title')
        i.add_css('price', 'div.price > span')
        i.add_css('size', 'td.attr-value')
        i.add_css('time', 'span.status')
        
        i.add_css('selector', 'ol.breadcrumb > li > a > span')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        
        i.add_css('content_1', 'div.shortdesc')
        i.add_css('content_2', 'div.desc')

        i.add_css('content_1_html', 'div.shortdesc')
        i.add_css('content_2_html', 'div.desc')

        for img in response.css('div.slick-slide > div > div > div > picture > img::attr(src)'):
            i.add_value('image_urls', img.get())
        
        return i.load_item()
