from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class FeliciSpider(BaseSpider):

    name = 'Felici-caballi'
    address = '7000096'
    allowed_domains = ['felici-caballi.de']
    start_urls = ['https://www.felici-caballi.de/shop/']

    def parse(self, response):
        for item in response.css('ul.products > li.product > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        for item in response.css('select#groesse > option::attr(value)'):
            yield self.parse_product(
                response=self.select(
                    url=response.url,
                    select='select#groesse',
                    option=item.get(),
                    delay=10
                ),
                parent=response.css('span.sku').get()
            )


    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'FC'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.sku')
        i.add_css('sid', 'span.sku')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product_title')
        i.add_css('price', 'span.amount > bdi')
        i.add_css('size', 'div.woocommerce-variation-description > p')

        i.add_css('selector', 'div.fusion-breadcrumbs > span > a > span')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Inhaltsstoffe')
        i.add_value('title_3', 'Beschreibung')
        i.add_value('title_4', 'Zusätzliche Informationen')

        i.add_css('content_1', 'div.woocommerce-product-details__short-description > p:nth-child(1)')
        i.add_css('content_2', 'div.woocommerce-product-details__short-description > p:nth-child(2)')
        i.add_css('content_3', 'div#tab-description')
        i.add_css('content_4', 'div#tab-additional_information')
        
        i.add_css('content_1_html', 'div.woocommerce-product-details__short-description > p:nth-child(1)')
        i.add_css('content_2_html', 'div.woocommerce-product-details__short-description > p:nth-child(2)')
        i.add_css('content_3_html', 'div#tab-description')
        i.add_css('content_4_html', 'div#tab-additional_information')
        
        for img in response.css('div.woocommerce-product-gallery__image > img::attr(src)'):
            i.add_value('image_urls', img.get())

        return i.load_item()
