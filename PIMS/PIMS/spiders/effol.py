from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class EffolSpider(BaseSpider):

    name = 'effol'
    address = '7022500'
    allowed_domains = ['effol.com']
    start_urls = ['https://www.effol.com/de-de/de_DE/']

    def parse(self, response):
        item = response.css('ul.cat-nav > li > ul > li > a::attr(href)')
        yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page(url=response.url, delay=10)

        for item in page.css('div.product > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        for item in response.css('div#sizeBoxes > select > option::attr(value)'):
            yield self.parse_product(
                response=self.select(
                    url=response.url,
                    select='div#sizeBoxes > select',
                    option=item.get(),
                    delay=20,
                    cookies='Alle akzeptieren'
                ),
                parent=response.css('div.prodCode > div > span').get()
            )

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'EQ'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'div.prodCode > div > span')
        i.add_css('sid', 'div.prodCode > div > span')
        i.add_value('parent', parent)
        i.add_css('title', 'div.prodTitle > div > h1')
        i.add_css('price', 'div.prodPrice > span.priceValue')
        i.add_css('size', 'div.prodWeight > span')
        i.add_css('time', 'p.delivery-time-info')
        
        i.add_css('selector', 'div.pathLine > div > a:not(:last-child)')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        
        i.add_css('content_1', 'div.shortDesc')
        i.add_css('content_2', 'div.longDesc')

        i.add_css('content_1_html', 'div.shortDesc')
        i.add_css('content_2_html', 'div.longDesc')

        i.add_value('image_urls', response.css('a.pv-main-img-link::attr(href)').get())
        
        return i.load_item()
