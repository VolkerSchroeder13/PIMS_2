from PIMS.items import Product
from scrapy import Spider, Request
from scrapy.loader import ItemLoader


class AgrobsSpider(Spider):

    name = 'agrobs'
    allowed_domains = ['agrobs.de']
    start_urls = ['https://www.agrobs.de/de/']

    def parse(self, response):
        for category in response.css('nav.primary_navigation > div > :nth-child(1) > li > a::attr(href)'):
            yield Request(url=response.urljoin(category.get()), callback=self.parse_category)

    def parse_category(self, response):
        for sub_category in response.css('div.categorybox > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(sub_category.get()), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        for product in response.css('div.itembox > div > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(product.get()), callback=self.parse_product)

        next = response.css('div.page_switch > a.page_switch_next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_subcategory)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.add_value('brand', self.name)
        i.add_value('id', str(response.url).split('-')[-1].split('/')[0])
        i.add_css('size', 'li:contains("Handelsform")')
        i.add_css('title', 'h1.itemcardHeadline')
        
        i.add_css('selector', 'div.breadcrumbWrapper > span > a ::text')

        i.add_css('short_description', 'div.itemcardBullets > div:nth-child(1) div:nth-child(3)')
        i.add_css('description', 'div.itemDetailsDescription.beschreibung > div > div')
        i.add_css('recommendation', 'div.itemDetailsDescription.fuetterungsempfehlung > div')
        i.add_css('composition', 'div.itemDetailsDescription.inhaltsstoffe > div > div')
        
        i.add_value('recommendation_title', 'Fütterungsempfehlung')
        i.add_value('composition_title', 'Inhaltsstoffe')

        i.add_css('short_description_html', 'div.itemcardBullets > div:nth-child(1) div:nth-child(3)')
        i.add_css('description_html', 'div.itemDetailsDescription > div > div')
        i.add_css('recommendation_html', 'div.itemDetailsDescription.fuetterungsempfehlung > div')
        i.add_css('composition_html', 'div.itemDetailsDescription.inhaltsstoffe > div > div')
        
        for img in response.css('div.itemcard_images > div > div > div > img::attr(src)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
