from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class WeyrauchSpider(BaseSpider):

    name = 'weyrauch'
    address = '7017800'
    allowed_domains = ['shop.dr-susanne-weyrauch.de']
    start_urls = ['https://shop.dr-susanne-weyrauch.de']

    def parse(self, response):
        for item in response.css('div.navigation--list-wrapper > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.listing > div > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

        next = response.css('div.listing--bottom-paging > div > a.paging--link.paging--next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        pages = self.click(
            url=response.url,
            selector='div.configurator--variant > form > div > input',
            delay=10
        )

        for page in pages:
            yield self.parse_product(
                response=page, 
                parent=page.css('ul.product--base-info > li > span').get()
            )
           
    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = ''
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'ul.product--base-info > li > span')
        i.add_css('sid', 'ul.product--base-info > li > span')
        i.add_value('parent', parent)
        i.add_css('title', 'div.product--info > h1.product--title')
        i.add_css('price', 'div.product--price > span.price--content')
        i.add_css('size', 'div.product--price.price--unit')
        i.add_css('time', 'p.delivery--information > span.delivery--text')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_value('title_1', 'Beschreibung')
        i.add_value('title_2', 'Inhaltsstoffe')
        
        i.add_css('content_1', 'div.content--description')
        i.add_css('content_2', 'div.content--inhaltsstoffe')
        
        i.add_css('content_1_html', 'div.content--description')
        i.add_css('content_2_html', 'div.content--inhaltsstoffe')
        
        for img in response.css('div.image-slider--container > div > div > span::attr(data-img-large)'):
            i.add_value('image_urls', img.get())
        
        return i.load_item()
