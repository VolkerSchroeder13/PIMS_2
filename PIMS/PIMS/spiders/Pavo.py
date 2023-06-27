from PIMS.spiders.base import BaseSpider
from scrapy.loader import ItemLoader
from PIMS.items import Product
from scrapy import Request
import json


class PavoSpider(BaseSpider):

    name = 'Pavo'
    address = '7029500'
    allowed_domains = ['pavo-futter.de']
    start_urls = ['https://www.pavo-futter.de']

    def parse(self, response):
        for item in response.css('div.navigation > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('div.product-tile__image > a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

        next = response.css('a.pagination-next::attr(href)')
        if next is not None:
            yield Request(url=response.urljoin(next.get()), callback=self.parse_category)

    def parse_variation(self, response):
        pages = self.click(
            url=response.url, 
            selector='div.product-info__variants > label', 
            delay=10
        )

        for page in pages:
            data = json.loads(page.css('script[type="application/ld+json"]::text').get())
            yield self.parse_product(response=page, parent=data['url'].split("=")[-1])

    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)
        
        data = json.loads(response.css('script[type="application/ld+json"]::text').get())

        i.context['prefix'] = 'PV'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_value('id', data['url'].split("=")[-1])
        i.add_value('sid',  data['url'].split("=")[-1])
        i.add_value('parent', parent)
        i.add_css('title', 'div.product-info__title')
        i.add_css('price', 'label.product-info-variant.active div.product-offer__price > span')
        i.add_css('size', 'label.product-info-variant.active dl.product-info-variant__description-specs > dd')
        
        i.add_css('selector', 'div.breadcrumbs-component > a::text')

        i.add_value('title_1', 'Untertitel')
        i.add_value('title_2', 'Kurzbeschreibung')
        i.add_value('title_3', 'Beschreibung')
        i.add_value('title_4', 'Spezifikation')
        i.add_value('title_5', 'Fütterungsempfehlung')

        tabs = self.click(
            url=data['url'], 
            selector='div.product-details__tabs > button', 
            delay=10
        )

        i.add_css('content_1', 'h2.product-info__subtitle')
        i.add_css('content_2', 'p.product-info__description-text')
        i.add_css('content_1_html', 'h2.product-info__subtitle')
        i.add_css('content_2_html', 'p.product-info__description-text')
        
        if len(tabs) >= 1:
            i.add_value('content_3', tabs[0].css('div.product-details__content').get())
            i.add_value('content_3_html', tabs[0].css('div.product-details__content').get())
        
        if len(tabs) >= 2:
            i.add_value('content_4', tabs[1].css('div.product-details__content').get())
            i.add_value('content_4_html', tabs[1].css('div.product-details__content').get())

        if len(tabs) >= 3:
            i.add_value('content_5', tabs[2].css('div.product-details__content').get())
            i.add_value('content_5_html', tabs[2].css('div.product-details__content').get())
        

        for img in response.css('div.keen-slider > div > div > div > figure > picture > img::attr(src)'):
            i.add_value('image_urls', img.get())

        return i.load_item()
