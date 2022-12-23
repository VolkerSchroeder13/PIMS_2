from PIMS.items import Product
from scrapy import Spider, Request
from scrapy.loader import ItemLoader


class ArdapcareSpider(Spider):

    name = 'ardapcare'
    allowed_domains = ['ardapcare.com']
    start_urls = ['https://ardapcare.com']

    def parse(self, response):
        for category in response.css('div.site-nav__dropdown > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(category.get()), callback=self.parse_category)

    def parse_category(self, response):
        for product in response.css('ul.grid > li > div > a::attr(href)'):
            yield Request(url=response.urljoin(product.get()), callback=self.parse_variation)

        next = response.css('ul.pagination > li:nth-child(3) > a::attr(href)')
        if next is not None:    
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        for product in response.css('select.product-form__variants > option::attr(value)'):
            yield Request(url=(response.url+'/?variant='+product.get()), callback=self.parse_product)

    def parse_product(self, response):
        item = ItemLoader(item=Product(), response=response)

        item.add_value('brand', self.name)
        item.add_css('id', 'span.variant-sku')
        item.add_css('title', 'h1.product-single__title')
        item.add_css('price', 'span.price-item--regular')
        item.add_css('time', 'div.product-single__description > p')
        item.add_css('size', 'select.single-option-selector > option[selected]::attr(value)')

        item.add_css('short_description', 'div.product-single__description > ul')
        item.add_css('short_description_html', 'div.product-single__description > ul')

        for img in response.css('div.grid__item.product-single__media-group > div > div > img::attr("data-src")'):
            item.add_value('image_urls', response.urljoin(img.get()))

        yield item.load_item()
