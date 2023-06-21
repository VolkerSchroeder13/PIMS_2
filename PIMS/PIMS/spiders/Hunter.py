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
        page = self.page(url=response.url, delay=5)

        for item in page.css('nav > div > div > ul.navigation--list > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page(url=response.url, delay=5)

        for item in page.css('a.dig-pub--link::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        page = self.page_scroll_down(url=response.url, delay=5, cookies='span#cmpbntyestxt')

        for item in page.css('div.product--detail-btn > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_variation)

    def parse_variation(self, response):
        pages = self.click(
            url=response.url, 
            selector='div.variant--option > label > span',
            delay=5,
            cookies='span#cmpbntyestxt'
        )

        for page in pages:
            yield self.parse_product(response=page, parent=page.css('span.entry--content').get())

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'HN'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.entry--content')
        i.add_css('sid', 'span.entry--content')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'span.price--content')
        i.add_css('time', 'span.delivery--text')
        i.add_css('size', 'div.product--configurator > div > form > div:nth-child(2) > div.variant--name > span')

        i.add_value('title_1', 'Produktinformationen')
        i.add_value('title_1', 'Messanleitung')
        i.add_value('title_1', 'Größentabelle')

        i.add_css('content_1', 'div.tab-menu--product > div.tab--container-list > div:nth-child(1)')
        i.add_css('content_2', 'div.tab-menu--product > div.tab--container-list > div:nth-child(2)')
        i.add_css('content_3', 'div.tab-menu--product > div.tab--container-list > div:nth-child(3)')

        i.add_css('content_1_html', 'div.tab-menu--product > div.tab--container-list > div:nth-child(1)')
        i.add_css('content_2_html', 'div.tab-menu--product > div.tab--container-list > div:nth-child(2)')
        i.add_css('content_3_html', 'div.tab-menu--product > div.tab--container-list > div:nth-child(3)')

        return i.load_item()
