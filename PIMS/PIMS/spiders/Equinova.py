from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class EquinovaSpider(Spider):

    name = 'Equinova'
    address = '7000017'
    allowed_domains = ['equinova.de']
    start_urls = ['https://www.equinova.de/']

    def parse(self, response):
        for item in response.css('div.advanced-menu > div.menu--container > div > ul > li > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product--box > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'EO'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'li.entry--sku > span')
        i.add_css('sid', 'li.entry--sku > span')
        i.add_value('parent', None)
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'span.price--content')
        i.add_css('size', 'div.price--unit')
        i.add_css('time', 'span.delivery--text')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_value('title_1', 'Beschreibung')
        i.add_value('title_2', 'Deklaration')
        i.add_value('title_3', 'Fütterungsempfehlung')
        
        i.add_css('content_1', 'div.detail--tab--container > div.tab-menu--product > div.tab--container-list > div:nth-child(1) > div.tab--content > :nth-child(2)')
        i.add_css('content_2', 'div.detail--tab--container > div.tab-menu--product > div.tab--container-list > div:nth-child(2) > div.tab--content > :nth-child(2)')
        i.add_css('content_3', 'div.detail--tab--container > div.tab-menu--product > div.tab--container-list > div:nth-child(3) > div.tab--content > :nth-child(2)')
        
        i.add_css('content_1_html', 'div.detail--tab--container > div.tab-menu--product > div.tab--container-list > div:nth-child(1) > div.tab--content > :nth-child(2)')
        i.add_css('content_2_html', 'div.detail--tab--container > div.tab-menu--product > div.tab--container-list > div:nth-child(2) > div.tab--content > :nth-child(2)')
        i.add_css('content_3_html', 'div.detail--tab--container > div.tab-menu--product > div.tab--container-list > div:nth-child(3) > div.tab--content > :nth-child(2)')
        
        for img in response.css('span.image--element::attr(data-img-large)'):
            i.add_value('image_urls', img.get())
        
        yield i.load_item()
