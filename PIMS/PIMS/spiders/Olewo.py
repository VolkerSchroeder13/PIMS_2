from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class OlewoSpider(BaseSpider):

    name = 'Olewo'
    address = '7019400'
    allowed_domains = ['olewo.de']
    start_urls = ['https://www.olewo.de']

    def parse(self, response):
        for item in response.css('ul.navigation--list > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page_scroll_down(url=response.url, delay=10)

        for item in page.css('div.product--info > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        page = self.page(url=response.url, delay=10)
        
        for item in response.css('div.js--fancy-select > select > option::attr(value)'):
            yield self.parse_product(
                response=self.select(
                    url=response.url,
                    select='div.product--configurator select',
                    option=item.get(),
                    delay=20
                ), 
                parent=response.css('span.entry--content').get()
            )
       
        yield self.parse_product(response=page, parent=page.css('span.entry--content').get())

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'OL'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.entry--content')
        i.add_css('sid', 'span.entry--content')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product_title')
        i.add_css('price', 'span.price--content')
        i.add_css('size', 'div.product--price')
        i.add_css('time', 'span.delivery--text')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_value('title_1', 'Beschreibung')
        i.add_css('content_1', 'div.product--description')
        i.add_css('content_1_html', 'div.product--description')
        
        for img in response.css('div.image--box > span > span > img::attr(srcset)'):
            i.add_value('image_urls', img.get())

        return i.load_item()
