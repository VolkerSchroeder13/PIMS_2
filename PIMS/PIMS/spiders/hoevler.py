from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class HoevlerSpider(Spider):

    name = 'hoevler'
    address = '7000017'
    allowed_domains = ['hoeveler.com']
    start_urls = ['https://www.hoeveler.com/home.html']

    def parse(self, response):
        for item in response.css('div#col_875 > ul > li > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.listing > div > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'EO'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', ' div.product--price.ordernumber > span')
        i.add_css('title', 'h1.product--title')
        i.add_css('price', 'div,.product--price > span')
        i.add_css('size', 'div.product--price.price--unit')
        
        i.add_css('selector', 'ul.breadcrumb--list > li > a > span')

        i.add_css('short_description', 'div.product--keywords')
        i.add_css('description', 'div.content--description')
        i.add_css('recommendation', 'div.product--description')
        i.add_css('composition', 'div.product--content')
       
        i.add_value('recommendation_title', 'Deklaration')
        i.add_value('composition_title', 'Fütterungsempfehlung')
     
        i.add_css('short_description_html', 'div.product--keywords')
        i.add_css('description_html', 'div.content--description')
        i.add_css('recommendation_html', 'div.product--description')
        i.add_css('composition_html', 'div.product--content')
    
        for img in response.css('div.image--box > span > span > img::attr(srcset)'):
            i.add_value('image_urls', img.get())

        yield i.load_item()
