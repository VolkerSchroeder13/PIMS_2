from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class ErlerZimmerSpider(BaseSpider):

    name = 'Erler-zimmer'
    address = '7021000'
    allowed_domains = ['erler-zimmer.de']
    start_urls = ['https://erler-zimmer.de/produkte/']

    def parse(self, response):
        page = self.page(url=response.url, delay=10)

        for item in page.css('div.card-container > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product--info > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

        next = response.css('a.paging--next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'EZ'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'li.entry--sku > span.entry--content')
        i.add_css('sid', 'li.entry--sku > span.entry--content')
        i.add_value('parent', None)
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'span.price--content')
        i.add_css('time', 'span.delivery--text')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_value('title_1', 'Vorteile')
        i.add_value('title_2', 'Beschreibung')
        
        i.add_css('content_1', 'div#usp-artikelbox')
        i.add_css('content_2', 'div.content--description')
        
        i.add_css('content_1_html', 'div#usp-artikelbox')
        i.add_css('content_2_html', 'div.content--description')
        
        for img in response.css('span.image--media > img::attr(srcset)'):
            i.add_value('image_urls', img.get())
        
        yield i.load_item()
