import json
from PIMS.items import Product
from scrapy import Spider, Request
from scrapy.loader import ItemLoader


class AniforteSpider(Spider):

    name = 'aniforte'
    allowed_domains = ['aniforte.de']
    start_urls = ['https://www.aniforte.de']

    def parse(self, response):
        for category in response.css('div.Header__Wrapper > nav > li > a::attr(href)'):
            yield Request(url=response.urljoin(category.get()), callback=self.parse_category)

    def parse_category(self, response):
        for sub_category in response.css('div.Header__Wrapper > nav > ul.sub-menu_active > li > a::attr(href)'):
            yield Request(url=response.urljoin(sub_category.get()), callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        for menu in response.css('ul.sub-menu_active > ul > ul > li > a::attr(href)'):
            yield Request(url=response.urljoin(menu.get()), callback=self.parse_submenu)

    def parse_submenu(self, response):
        for product in response.css('div.ProductList > div > div > div > a::attr(href)'):
            yield Request(url=response.urljoin(product.get()), callback=self.parse_variation)

        next = response.css('div.Pagination__Nav > a[rel=next]::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_submenu)

    def parse_variation(self, response):
        for product in response.css('div.ProductForm__Option > div > select > option::attr(value)'):
            yield Request(url=(response.url+'?variant='+product.get()), callback=self.parse_product)

    def parse_product(self, response):
        i = ItemLoader(item=Product(), response=response)
        
        data = json.loads(response.css('script[type="application/ld+json"]::text').get())
        i.add_value('brand', self.name)
        i.add_value('id', data['sku'])
        i.add_css('title', 'h2.ProductMeta__Title')
        i.add_css('price', 'span.ProductMeta__Price')
        i.add_css('size', 'div.ProductForm__Variants > div.ProductForm__Option > ul > li > input[checked]::attr(value)')
        i.add_css('time', 'div.ProductMeta > div.price_and_info_container > :nth-child(3)')
        
        i.add_css('selector', 'div.Header__Wrapper a.link_active')

        i.add_css('short_description', 'ul.ProductMeta__usps')
        i.add_css('description', 'div.Product__Tabs > div > button:contains("Beschreibung") ~ div')
        i.add_css('recommendation', 'div.Product__Tabs > div > button:contains("Fütterungsempfehlung") ~ div')
        i.add_css('composition', 'div.Product__Tabs > div > button:contains("Zusammensetzung") ~ div')
        i.add_css('usage', 'div.Product__Tabs > div > button:contains("Anwendung") ~ div')
        i.add_css('safety', 'div.Product__Tabs > div > button:contains("Produkthinweis") ~ div')
        
        i.add_value('recommendation_title', 'Fütterungsempfehlung')
        i.add_value('composition_title', 'Zusammensetzung')
        i.add_value('usage_title', 'Anwendung')
        i.add_value('safety_title', 'Produkthinweis')

        i.add_css('short_description_html', 'ul.ProductMeta__usps')
        i.add_css('description_html', 'div.Product__Tabs > div > button:contains("Beschreibung") ~ div')
        i.add_css('recommendation_html', 'div.Product__Tabs > div > button:contains("Fütterungsempfehlung") ~ div')
        i.add_css('composition_html', 'div.Product__Tabs > div > button:contains("Zusammensetzung") ~ div')
        i.add_css('usage_html', 'div.Product__Tabs > div > button:contains("Anwendung") ~ div')
        i.add_css('safety_html', 'div.Product__Tabs > div > button:contains("Produkthinweis") ~ div')
        
        for img in response.css('div.Product__Slideshow > div > div > img::attr(data-original-src)'):
            i.add_value('image_urls', response.urljoin(img.get()))
        
        yield i.load_item()
