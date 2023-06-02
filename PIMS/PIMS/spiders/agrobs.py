from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class AgrobsSpider(Spider):

    name = 'Agrobs'
    address = '7000083'
    allowed_domains = ['agrobs.de']
    start_urls = ['https://www.agrobs.de/de/']

    def parse(self, response):
        for item in response.css('nav.primary_navigation > div > :nth-child(1) > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.categorybox > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        for item in response.css('div.itembox > div > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

        next = response.css('div.page_switch > a.page_switch_next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_subcategory)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'AG'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_value('id', str(response.url).split('-')[-1].split('/')[0])
        i.add_value('sid', str(response.url).split('-')[-1].split('/')[0])
        i.add_css('size', 'li:contains("Handelsform")')
        i.add_css('title', 'h1.itemcardHeadline')
        
        i.add_css('selector', 'div.breadcrumbWrapper > span > a ::text')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Fütterungsempfehlung')
        i.add_value('title_4', 'Inhaltsstoffe')

        i.add_css('content_1', 'div.itemcardBullets > div:nth-child(1) div:nth-child(3)')
        i.add_css('content_2', 'div.itemDetailsDescription.beschreibung > div > div')
        i.add_css('content_3', 'div.itemDetailsDescription.fuetterungsempfehlung > div')
        i.add_css('content_4', 'div.itemDetailsDescription.inhaltsstoffe > div > div')
        
        i.add_css('content_1_html', 'div.itemcardBullets > div:nth-child(1) div:nth-child(3)')
        i.add_css('content_2_html', 'div.itemDetailsDescription > div > div')
        i.add_css('content_3_html', 'div.itemDetailsDescription.fuetterungsempfehlung > div')
        i.add_css('content_4_html', 'div.itemDetailsDescription.inhaltsstoffe > div > div')
        
        for img in response.css('div.itemcard_images > div > div > div > img::attr(src)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
