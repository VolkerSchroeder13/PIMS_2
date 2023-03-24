from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class ArdapcareSpider(Spider):

    name = 'ardapcare'
    address = '7025100'
    allowed_domains = ['ardapcare.com']
    start_urls = ['https://ardapcare.com']

    def parse(self, response):
        for item in response.css('div.site-nav__dropdown > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('ul.grid > li > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

        next = response.css('ul.pagination > li:nth-child(3) > a::attr(href)')
        if next is not None:    
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        for item in response.css('select.product-form__variants > option::attr(value)'):
            yield Request(
                url=(response.url+'/?variant='+item.get()), 
                callback=self.parse_product,
                cb_kwargs=dict(parent=response.css('span.variant-sku').get())
            )

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), response=response)

        i.context['prefix'] = 'AR'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.variant-sku')
        i.add_value('parent', parent)
        i.add_css('title', 'h1.product-single__title')
        i.add_css('price', 'span.price-item--regular')
        i.add_css('time', 'div.product-single__description > p')
        i.add_css('size', 'select.single-option-selector > option[selected]::attr(value)')

        i.add_value('title_1', 'Kurzbeschreibung')

        i.add_css('content_1', 'div.product-single__description > ul')
        i.add_css('content_1_html', 'div.product-single__description > ul')

        yield i.load_item()
