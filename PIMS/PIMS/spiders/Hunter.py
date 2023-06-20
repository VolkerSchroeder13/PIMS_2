from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class HunterSpider(BaseSpider):

    name = 'Hunter'
    address = '7000098'
    allowed_domains = ['wirliebenhunter.de']
    start_urls = ['https://www.wirliebenhunter.de/']

    def parse(self, response):
        page = self.page(url=response.url, delay=10)

        for item in page.css('ul.navigation--list > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page(url=response.url, delay=10)

        for item in page.css('a.dig-pub--link::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        page = self.page_scroll_down(url=response.url, delay=10)

        for item in page.css('div.product--detail-btn > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_variation)

    def parse_variation(self, response):
        pages = self.click(
            url=response.url, 
            selector='',
            delay=10
        )

        for page in pages:
            pass

    def parse_subvariation(self, response):
        page = self.page(url=response.url, delay=10)

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), response=response)

        i.context['prefix'] = 'HN'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.variant-sku')
        i.add_css('sid', 'span.variant-sku')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product-single__title')
        i.add_css('price', 'span.price-item--regular')
        i.add_css('time', 'div.product-single__description > p')
        i.add_css('size', 'select.single-option-selector > option[selected]::attr(value)')

        i.add_value('title_1', 'Kurzbeschreibung')

        i.add_css('content_1', 'div.product-single__description > ul')
        i.add_css('content_1_html', 'div.product-single__description > ul')

        yield i.load_item()
