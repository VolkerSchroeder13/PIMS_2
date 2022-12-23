from PIMS.items import Product
from scrapy import Spider, Request
from scrapy.loader import ItemLoader


class WaldkraftSpider(Spider):

    name = 'waldkraft'
    allowed_domains = ['waldkraft.bio']
    start_urls = ['http://waldkraft.bio/']

    def parse(self, response):
        for category in response.css('div.navigation--list-wrapper > ul > li > a::attr(href)'):
            yield Request(url=category.get(), callback=self.parse_category)

    def parse_category(self, response):
        products = response.css('div.box--content > div.product--info > a::attr(href)')
        for product in products:
            yield Request(url=product.get(), callback=self.parse_product)

        if products != []:
            try: yield Request(url=(response.url).split('?p=')[0]+"?p="+str(int((response.url).split('?p=')[-1])+1), callback=self.parse_category)
            except: yield Request(url=(response.url).split('?p=')[0]+"?p=1", callback=self.parse_category)

    def parse_product(self, response):
        item = ItemLoader(item=Product(), response=response)
        
        item.add_value('brand', self.name)
        item.add_css('id', 'span.entry--content')
        item.add_css('title', 'h1.product--title')
        item.add_css('price', 'span.price--content > meta::attr(content)')
        item.add_css('size', 'div.product--price.price--unit::text')
        item.add_css('time', 'span.delivery--text')

        item.add_css('short_description', 'div.mill-article-advantages')
        item.add_css('description', 'div.tab--container.has--content.is--active')

        item.add_css('short_description_html', 'div.mill-article-advantages')
        item.add_css('description_html', 'div.tab--container.has--content.is--active')
     
        for img in response.css('div.image-slider--container > div > div > span > span > img::attr(srcset)'):
            item.add_value('image_urls', img.get())

        yield item.load_item()