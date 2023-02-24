from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class BallistolSpider(Spider):

    name = 'ballistol'
    allowed_domains = ['ballistol.de']
    start_urls = ['https://ballistol.de/']

    def parse(self, response):
        for category in response.css('div.menu--container:nth-child(2) > div.content--wrapper > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(category.get()), callback=self.parse_category)

    def parse_category(self, response):
        products = response.css('div.listing--container > div.listing > div > div > div > a::attr(href)')
        for product in products:
            yield Request(url=response.urljoin(product.get()), callback=self.parse_product)

        next = response.css('a.paging--link::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
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

        yield i.load_item()

