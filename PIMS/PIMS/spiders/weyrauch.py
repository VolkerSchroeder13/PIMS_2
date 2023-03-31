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
        pass

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), response=response)
        
        i.context['prefix'] = ''
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_value('id', '')
        i.add_value('sid', '')
        i.add_value('parent', parent)
        i.add_css('title', 'h2.ProductMeta__Title')
        i.add_css('price', 'span.ProductMeta__Price')
        i.add_css('size', 'div.ProductForm__Variants > div.ProductForm__Option > ul > li > input[checked]::attr(value)')
        i.add_css('time', 'div.ProductMeta > div.price_and_info_container > :nth-child(3)')
        
        i.add_css('selector', 'div.Header__Wrapper a.link_active')

        i.add_value('title_1', 'Kurzbeschreibung')
        i.add_value('title_2', 'Beschreibung')
        i.add_value('title_3', 'Fütterungsempfehlung')
        i.add_value('title_4', 'Zusammensetzung')
        i.add_value('title_5', 'Anwendung')
        i.add_value('title_6', 'Produkthinweis')
        
        i.add_css('content_1', 'ul.ProductMeta__usps')
        i.add_css('content_2', 'div.Product__Tabs > div > button:contains("Beschreibung") ~ div')
        i.add_css('content_3', 'div.Product__Tabs > div > button:contains("Fütterungsempfehlung") ~ div')
        i.add_css('content_4', 'div.Product__Tabs > div > button:contains("Zusammensetzung") ~ div')
        i.add_css('content_5', 'div.Product__Tabs > div > button:contains("Anwendung") ~ div')
        i.add_css('content_6', 'div.Product__Tabs > div > button:contains("Produkthinweis") ~ div')
        
        i.add_css('content_1_html', 'ul.ProductMeta__usps')
        i.add_css('content_2_html', 'div.Product__Tabs > div > button:contains("Beschreibung") ~ div')
        i.add_css('content_3_html', 'div.Product__Tabs > div > button:contains("Fütterungsempfehlung") ~ div')
        i.add_css('content_4_html', 'div.Product__Tabs > div > button:contains("Zusammensetzung") ~ div')
        i.add_css('content_5_html', 'div.Product__Tabs > div > button:contains("Anwendung") ~ div')
        i.add_css('content_6_html', 'div.Product__Tabs > div > button:contains("Produkthinweis") ~ div')
        
        for img in response.css('div.Product__Slideshow > div > div > img::attr(data-original-src)'):
            i.add_value('image_urls', response.urljoin(img.get()))
        
        yield i.load_item()
