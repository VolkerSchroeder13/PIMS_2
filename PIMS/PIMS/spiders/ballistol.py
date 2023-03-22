from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class BallistolSpider(BaseSpider):

    name = 'ballistol'
    address = '7025200'
    allowed_domains = ['ballistol.de']
    start_urls = ['https://ballistol.de/']

    def parse(self, response):
        for item in response.css('div.menu--container:nth-child(2) > div.content--wrapper > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        items = response.css('div.listing--container > div.listing > div > div > div > a::attr(href)')
        for item in items:
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

        next = response.css('a.paging--link::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        page = self.page(url=response.url, delay=5)

        if response.css('div.product--configurator select').get() is not None:
            for item in response.css('div.product--configurator select option::attr(value)'):
                self.select(
                    url=response.url,
                    select='div.product--configurator select',
                    option=item.get(),
                    delay=10
                )
        
        yield self.parse_product(response=page)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'BA'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.entry--content')
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'span.price--content > meta::attr(content)')
        i.add_css('size', 'div.product--configurator > form > div > select > option[selected]')

        i.add_css('selector', 'span.breadcrumb--title')

        i.add_css('description', 'div.product--description > div.pro-desc')
        i.add_css('recommendation', 'div.properties--content--section > div.product--properties')
        i.add_css('safety', 'div.safety_instructions--content--section > div > div.si-desc')

        i.add_value('recommendation_title', 'Eigenschaften')
        i.add_value('safety_title', 'Gefahren- und Sicherheitshinweise')

        i.add_css('description_html', 'div.product--description > div.pro-desc')
        i.add_css('recommendation_html', 'div.properties--content--section > div.product--properties')
        i.add_css('safety_html', 'div.safety_instructions--content--section > div > div.si-desc')

        for img in response.css('div.image-slider--slide > div > span > span > img::attr(srcset)'):
            i.add_value('image_urls', img.get())

        return i.load_item()

