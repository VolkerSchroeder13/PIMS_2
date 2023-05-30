from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class FleischeslustSpider(BaseSpider):

    name = 'fleischeslust'
    address = '7002400'
    allowed_domains = ['fleischeslust-tiernahrung.de']
    start_urls = ['https://www.fleischeslust-tiernahrung.de/shop/']

    def parse(self, response):
        for item in response.css('ul.navigation--list > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product--info > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

        next = response.css('a.paging--next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        for item in response.css('div.product--configurator > form > div > select > option::attr(value)'):
            yield self.parse_product(
                response=self.select(
                    response.url, 
                    select='div.product--configurator > form > div > select',
                    option=item.get(),
                    delay=10,
                    cookies='button#CybotCookiebotDialogBodyButtonAccept'
                ),
                parent=response.css('span.entry--content').get()
            )

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
       
        i.context['prefix'] = 'FL'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.entry--content')
        i.add_css('sid', 'span.entry--content')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product--title')
        i.add_css('time', 'span.delivery--text')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_value('title_1', 'Beschreibung')
        i.add_css('content_1', 'div.content--description')
        i.add_css('content_1_html', 'div.content--description')
       
        for img in response.css('div.image-slider--container > div > div > span > span > img::attr(src)'):
            i.add_value('image_urls', img.get())
        
        return i.load_item()
