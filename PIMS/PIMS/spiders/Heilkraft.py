from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request


class HeilkraftSpider(BaseSpider):

    name = 'Heilkraft'
    address = '7024300'
    allowed_domains = ['heilkraft.online']
    start_urls = ['https://heilkraft.online']

    def parse(self, response):
        item = response.css('ul.navigation--list > li > a::attr(href)')
        yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product--info > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        for item in response.css('div.product--configurator > form > div > select > option::attr(value)'):
            yield self.parse_product(
                response=self.select(
                    url=response.url,
                    select='div.product--configurator > form > div > select',
                    option=item.get(),
                    delay=20,
                    cookies='a.cookie-permission--accept-button'
                ),
                parent=response.css('span.entry--content').get()
            )

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        i.context['prefix'] = 'HK'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.entry--content')
        i.add_css('sid', 'span.entry--content')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'span.price--content')
        i.add_css('size', 'div.product--configurator > form > div > select > option[selected]')
        i.add_css('time', 'span.delivery--text')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_value('title_1', 'Vorteile')
        i.add_value('title_2', 'Beschreibung')
        
        i.add_css('content_1', 'div.usp-artikelbox')
        i.add_css('content_2', 'div.product--description')
        
        i.add_css('content_1_html', 'div.usp-artikelbox')
        i.add_css('content_2_html', 'div.product--description')
        
        for img in response.css('div.image-slider--slide > div > span::attr(data-img-original)'):
            i.add_value('image_urls', img.get())
        
        return i.load_item()
