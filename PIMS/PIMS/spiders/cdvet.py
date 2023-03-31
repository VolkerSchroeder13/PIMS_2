from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class CdvetSpider(BaseSpider):

    name = 'cdvet'
    address = '7000010'
    allowed_domains = ['cdvet.de']
    start_urls = ['https://www.cdvet.de']

    def parse(self, response):
        for item in response.css('div.navigation-flyouts a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.card-body > div.product-info > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        self.parse_product(
            response=self.click(
                url=response.url,
                selectors=[''],
                delay=20
            ),
            parent=response.css('').get()
        )

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'CV'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.entry--content')
        i.add_css('sid', 'span.entry--content')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'span.price--content > meta::attr(content)')
        i.add_css('size', 'div.product--configurator > form > div > select > option[selected]')

        i.add_css('selector', 'span.breadcrumb--title')

        i.add_value('title_1', 'Beschreibung')
        i.add_value('title_2', 'Eigenschaften')
        i.add_value('title_3', 'Gefahren- und Sicherheitshinweise')

        i.add_css('content_1', 'div.product--description > div.pro-desc')
        i.add_css('content_2', 'div.properties--content--section > div.product--properties')
        i.add_css('content_3', 'div.safety_instructions--content--section > div > div.si-desc')

        i.add_css('content_1_html', 'div.product--description > div.pro-desc')
        i.add_css('content_2_html', 'div.properties--content--section > div.product--properties')
        i.add_css('content_3_html', 'div.safety_instructions--content--section > div > div.si-desc')

        for img in response.css('div.image-slider--slide > div > span > span > img::attr(srcset)'):
            i.add_value('image_urls', img.get())

        return i.load_item()

