from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class FatboySpider(BaseSpider):

    name = 'fatboy'
    address = '7022600'
    allowed_domains = ['fatboy.com']
    start_urls = ['https://www.fatboy.com/de-de']

    def parse(self, response):
        page = self.page(url=response.url, delay=5)
        
        for item in page.css('nav.navigation--desktop > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page(url=response.url, delay=5)
        
        for item in page.css('div.subcategory-link > div > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        page = self.page(url=response.url, delay=5)
        
        if page.css('button:contains("Mehr laden")').get() is not None:
            page = self.click(
                url=response.url, 
                buttons=['OK', 'Mehr laden'], 
                delay=10
            )
        
        for item in page.css('div.category-grid > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        page = self.page(url=response.url, delay=5)

        for item in page.css('div.variant-picker--container > div > div > a::attr(href)'):
            yield self.parse_product(
                response=self.page(
                    url=response.urljoin(item.get()),
                    delay=5
                )
            )

    def parse_product(self, response):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'FB'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'div.product-attributes > dl > dd:nth-child(2)')
        i.add_css('ean', 'div.product-attributes > dl > dd:nth-child(4)')
        i.add_css('title', 'h1.title')
        i.add_css('price', 'span.price')
        i.add_css('time', 'div.product-stock--status')

        i.add_css('selector', 'nav.nav__breadcrumbs > ul > li > span')

        i.add_css('short_description', 'h2.subtitle')
        i.add_css('description', 'div.product-variant-information-wide > div > div:nth-child(4)')
        i.add_css('recommendation', 'div.product-variant-information-wide > div > div:nth-child(2)')
        i.add_css('composition', 'div.product-variant-information-wide > div > div:nth-child(3)')
        i.add_css('usage', 'div.product-variant-information-wide > div > div:nth-child(5)')
        i.add_css('safety', 'div.product-variant-information-wide > div > div:nth-child(6)')

        i.add_value('recommendation_title', 'Produkteigenschaften')
        i.add_value('composition_title', 'Abmessungen')
        i.add_value('usage_title', 'Nutzerinformation')
        i.add_value('safety_title', 'Nachhaltigkeit')

        i.add_css('short_description_html', 'h2.subtitle')
        i.add_css('description_html', 'div.product-variant-information-wide > div > div:nth-child(4)')
        i.add_css('recommendation_html', 'div.product-variant-information-wide > div > div:nth-child(2)')
        i.add_css('composition_html', 'div.product-variant-information-wide > div > div:nth-child(3)')
        i.add_css('usage_html', 'div.product-variant-information-wide > div > div:nth-child(5)')
        i.add_css('safety_html', 'div.product-variant-information-wide > div > div:nth-child(6)')

        for img in response.css('div.main-image-container img::attr(src)'):
            i.add_value('image_urls', img.get())

        return i.load_item()

   
