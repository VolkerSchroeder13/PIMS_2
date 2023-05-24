from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
import json


class SanadogSpider(BaseSpider):

    name = 'sanadog'
    address = '7000097'
    allowed_domains = ['sanadog.com']
    start_urls = ['https://sanadog.com/']

    counter_products = 0
    counter_variations = 0
    counter_no_variations = 0
    counter_started = 0
    counter_finished = 0

    def parse(self, response):
        for item in response.css('ul.site-nav a::attr(href)'):
            yield Request(url=response.urljoin(item.get()), callback=self.parse_category)

    def parse_category(self, response):
        page = self.page_scroll_down(url=response.url, delay=4)
        for item in page.css('div.product-collection div.product-bottom a.product-title::attr(href)'):
            self.counter_products += 1
            # yield Request(url=response.urljoin(item.get()), callback=self.parse_variation)
            yield Request(url=response.urljoin(item.get()), callback=self.parse_product, cb_kwargs=dict(parent=None))

    def parse_variation(self, response):
        page = self.page(url=response.url, delay=4)
        root = page.css('div.sku-product > span::text').get()
        print(f'    DEBUG pv {response.url}')
        print(f'    DEBUG pv root {root}')
        variants = False
        for item in page.css('div.swatch-element:not(.soldout) > input.text::attr(data-value-sticky)'):
            self.counter_variations += 1
            variants = True
            yield Request(
                url=(response.url+'?variant='+item.get()),
                callback=self.parse_product,
                cb_kwargs=dict(parent=root)
            )
        if not variants:
            self.counter_no_variations += 1
            yield Request(
                url=(response.url),
                callback=self.parse_product,
                cb_kwargs=dict(parent=root)
            )


    def parse_product(self, response, parent):
        self.counter_started += 1
        print(f'    DEBUG pp {response.url}')
        print(f'    DEBUG root {parent}')
        page = self.page(url=response.url, delay=4)

        i = ItemLoader(item=Product(), selector=page)

        # TODO add SA prefix here and remove SANA prefix from id
        i.context['prefix'] = ''
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'div.sku-product > span')
        i.add_css('sid', 'div.sku-product > span')
        # i.add_value('parent', parent)
        i.add_css('parent', 'div.sku-product > span')
        i.add_css('title', 'h1.product-title > span')
        price = int(page.css('div.prices > input::attr(value)').get()) / 100
        i.add_value('price', str(price))
        # size = str(page.css('div.header.a- > :nth-child(2)::text').get()).replace('.', '')
        i.add_css('size', 'div.header.a- > :nth-child(2)::text')
        # TODO? add price time

        for item in page.css('script[type="application/ld+json"]::text').getall():
            selector = ""
            if '"@type": "BreadcrumbList"' in item:
                json_item = json.loads(item)
                for n in range(len(json_item['itemListElement']) - 1):
                    if n != 0:
                        selector += " "
                    selector += json_item['itemListElement'][n]['name']
                i.add_value('selector', selector)

        desc_tabs = page.css('ul.easytabs-tabs > li > span::text').getall()
        desc_tabs_count = len(desc_tabs)

        if(desc_tabs_count >= 1):
            i.add_value('title_1', desc_tabs[0])
            i.add_css('content_1', 'div.easytabs-contents > :nth-child(1) > div[role=tabpanel]')
            i.add_css('content_1_html', 'div.easytabs-contents > :nth-child(1) > div[role=tabpanel]')
        if(desc_tabs_count >= 2):
            i.add_value('title_2', desc_tabs[1])
            i.add_css('content_2', 'div.easytabs-contents > :nth-child(2) > div[role=tabpanel]')
            i.add_css('content_2_html', 'div.easytabs-contents > :nth-child(2) > div[role=tabpanel]')
        if(desc_tabs_count >= 3):
            i.add_value('title_3', desc_tabs[2])
            i.add_css('content_2', 'div.easytabs-contents > :nth-child(2) > div[role=tabpanel]')
            i.add_css('content_2_html', 'div.easytabs-contents > :nth-child(2) > div[role=tabpanel]')
        if(desc_tabs_count >= 4):
            i.add_value('title_4', desc_tabs[3])
            i.add_css('content_4', 'div.easytabs-contents > :nth-child(4) > div[role=tabpanel]')
            i.add_css('content_4_html', 'div.easytabs-contents > :nth-child(4) > div[role=tabpanel]')
        if(desc_tabs_count >= 5):
            i.add_value('title_5', desc_tabs[4])
            i.add_css('content_5', 'div.easytabs-contents > :nth-child(5) > div[role=tabpanel]')
            i.add_css('content_5_html', 'div.easytabs-contents > :nth-child(5) > div[role=tabpanel]')
        if(desc_tabs_count >= 6):
            i.add_value('title_6', desc_tabs[5])
            i.add_css('content_6', 'div.easytabs-contents > :nth-child(6) > div[role=tabpanel]')
            i.add_css('content_6_html', 'div.easytabs-contents > :nth-child(6) > div[role=tabpanel]')


        for img in page.css('a.fancybox[rel=gallery1]::attr(href)'):
            i.add_value('image_urls', response.urljoin(img.get()))

        yield i.load_item()
        self.counter_finished += 1
        print(f'    DEBUG counter_finished {self.counter_finished}')
        print(f'    DEBUG counter_started {self.counter_started}')
        print(f'    DEBUG counter_products {self.counter_products}')
        print(f'    DEBUG counter_variations {self.counter_variations}')
        print(f'    DEBUG counter_no_variations {self.counter_no_variations}')
        print(f'    DEBUG pp done {response.url}')

