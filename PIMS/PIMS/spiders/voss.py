from PIMS.items import Product
from scrapy import Spider, Request
from scrapy.loader import ItemLoader


class VossSpider(Spider):
    
    name = 'Voss'
    allowed_domains = ['weidezaun.info']
    start_urls = ['http://weidezaun.info/']

    def parse(self, response):
        for category in response.css('nav.navbar > ul > li > a::attr(href)').getall():
            yield Request(url=response.urljoin(category), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.col-xs-12.classic > div.col-xs-12.col-xs-3-landscape.col-sm-3.noPadding > a::attr(href)').getall():
            yield Request(url=response.urljoin(item), callback=self.parse_product)
        
        next = response.css('li.next-page > a::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_product(self, response):
        item = ItemLoader(item=Product(), response=response)
        
        item.add_value('brand', self.name)
        item.add_css('id', 'div.articlewrapper > div > div > span > span')
        item.add_css('title', 'div.articlewrapper > div > div > h1')
        item.add_css('price', 'div.price > span::attr(content)')
        item.add_css('time', 'span.deliverytime')

        item.add_css('short_description', 'div.checklist > ul')
        item.add_css('description', 'div.contentBox.beschreibungBox')
        item.add_css('recommendation', 'div.contentBox.detailsBox')
        item.add_css('usage', 'div.contentBox.aufeinblickBox')

        item.add_value('recommendation_title', 'Details')
        item.add_value('usage_title', 'Auf einen Blick')

        item.add_css('short_description_html', 'div.checklist > ul')
        item.add_css('description_html', 'div.contentBox.beschreibungBox')
        item.add_css('recommendation_html', 'div.contentBox.detailsBox')
        item.add_css('usage_html', 'div.contentBox.aufeinblickBox')

        for img in response.css('div.articleDetailsGallery > div > div > div > a::attr(href)'):
            item.add_value('image_urls', img.get())

        yield item.load_item()