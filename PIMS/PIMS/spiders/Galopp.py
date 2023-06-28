from scrapy.loader import ItemLoader
from scrapy import Spider, Request
from PIMS.items import Product


class GaloppSpider(Spider):

    name = 'Galopp'
    address = '7000017'
    allowed_domains = ['galopp-pferdefutter.de']
    start_urls = ['https://www.galopp-pferdefutter.de/']

    def parse(self, response):
        for item in response.css('div.nav-link > div.dropdown-menu > a::attr(href)'):
            yield Request(url=item.get(), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product-box > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = 'EO'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.product-detail-ordernumber')
        i.add_css('sid', 'span.product-detail-ordernumber')
        i.add_value('parent', None)
        i.add_css('title', 'h1.product-detail-name')
        i.add_css('price', 'p.product-detail-price')
        i.add_css('size', 'span.price-unit-content')
        i.add_css('time', 'p.delivery-information')
        
        i.add_css('selector', 'ol.breadcrumb > li > a > span')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Inhaltsstoffe')
        i.add_value('title_4', 'Fütterungsempfehlung')
        
        i.add_css('content_1', 'div.product-wordcloud')
        i.add_css('content_2', 'div.Product__Tabs > div > button:contains("Beschreibung") ~ div')
        i.add_css('content_3', 'div.Product__Tabs > div > button:contains("Fütterungsempfehlung") ~ div')
        i.add_css('content_4', 'div.Product__Tabs > div > button:contains("Zusammensetzung") ~ div')
        
        i.add_css('content_1_html', 'div.product-wordcloud')
        i.add_css('content_2_html', 'div.product-detail-description')
        i.add_css('content_3_html', 'div.owntabs-tab1-tab-pane-container')
        i.add_css('content_4_html', 'div.wntabs-tab2-tab-pane-container')
       
        for img in response.css('div.gallery-slider-item > img::attr(src)'):
            i.add_value('image_urls', img.get())
        
        yield i.load_item()
