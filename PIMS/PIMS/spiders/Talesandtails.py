from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
import json


class SanadogSpider(BaseSpider):

    name = 'Talesandtails'
    address = '7028700'
    allowed_domains = ['talesandtails.de']
    start_urls = ['https://talesandtails.de/']

    def parse(self, response):
        for item in response.css(''):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page_scroll_down(url=response.url, delay=4)
        for item in page.css(''):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)

    def parse_variation(self, response):
        root = response.css('').get()
        vars = response.css('').getall()
        vars.append('')
        for item in vars:
            yield Request(
                url=(response.url+'?variant='+item),
                callback=self.parse_product,
                cb_kwargs=dict(parent=root)
            )


    def parse_product(self, response, parent):
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'TL'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        # id = response.css('div.sku-product > span::text').get()
        # i.add_value('id', id.replace('SANA', ''))
        # i.add_value('sid', id.replace('SANA', ''))
        # i.add_value('parent', parent.replace('SANA', 'SA'))
        # i.add_css('title', 'h1.product-title > span')
        # price = float(response.css('div.prices > input::attr(value)').get()) / 100
        # i.add_value('price', str(price).replace('.', ','))
        # i.add_css('size', 'div.header.a- > :nth-child(2)::text')

        # for item in response.css('script[type="application/ld+json"]::text').getall():
        #     selector = ""
        #     if '"@type": "BreadcrumbList"' in item:
        #         json_item = json.loads(item)
        #         for n in range(len(json_item['itemListElement']) - 1):
        #             if n != 0:
        #                 selector += " "
        #             selector += json_item['itemListElement'][n]['name']
        #         i.add_value('selector', selector)

        # desc_tabs = response.css('').getall()
        # desc_tabs_count = len(desc_tabs)

        # if(desc_tabs_count >= 1):
        #     i.add_value('title_1', desc_tabs[0])
        #     i.add_css('content_1', '')
        #     i.add_css('content_1_html', '')
        # if(desc_tabs_count >= 2):
        #     i.add_value('title_2', desc_tabs[1])
        #     i.add_css('content_2', '')
        #     i.add_css('content_2_html', '')
        # if(desc_tabs_count >= 3):
        #     i.add_value('title_3', desc_tabs[2])
        #     i.add_css('content_2', '')
        #     i.add_css('content_2_html', '')
        # if(desc_tabs_count >= 4):
        #     i.add_value('title_4', desc_tabs[3])
        #     i.add_css('content_4', '')
        #     i.add_css('content_4_html', '')
        # if(desc_tabs_count >= 5):
        #     i.add_value('title_5', desc_tabs[4])
        #     i.add_css('content_5', '')
        #     i.add_css('content_5_html', '')
        # if(desc_tabs_count >= 6):
        #     i.add_value('title_6', desc_tabs[5])
        #     i.add_css('content_6', '')
        #     i.add_css('content_6_html', '')


        # for img in response.css(''):
        #     i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
