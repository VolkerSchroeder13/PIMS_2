from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
from time import sleep
import json


class VetripharmSpider(BaseSpider):
    custom_settings = {
        # "DOWNLOAD_DELAY": "1.5",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    name = 'Vetripharm'
    address = '7017900'
    allowed_domains = ['vetripharm.de']
    start_urls = ['https://vetripharm.de/de/']

    visited_products = []
    visited_variations = []

    def search_json_item(self, contained_str, page, script_selector):
        json_item = None
        for script in page.css(script_selector).getall():
            if contained_str in script:
                json_item = json.loads(script)
        return json_item

    def parse(self, response):
        for href in response.css('li[title="produkte"] ul.uk-nav li a::attr(href)').getall():
            if(href == '#'):
                continue
            yield Request(url=response.urljoin(href), callback=self.parse_category)

    def parse_category(self, response):
        urls = []
        for href in response.css('a.btn-success::attr(href)').getall():
            urls.append(response.urljoin(href))
        urls = list(filter(lambda url: url not in self.visited_products, urls))
        self.visited_products.extend(urls)
        for url in urls:
            yield Request(url=url, callback=self.parse_variation)

    def parse_variation(self, response):
        parent = response.css('span.sku::text').get()
        selects = response.css('select[name*="product_option"]::attr(name)').getall()
        if len(selects) == 1:
            quantity_select = selects[0]
            quantity_select_selector = f'select[name="{quantity_select}"]'
            quantity_options = response.css(f'{quantity_select_selector} option::attr(value)').getall()
            for quantity in quantity_options:
                    page = self.select(response.url, quantity_select_selector, quantity, 1, 'a.cpnb-accept-btn')
                    yield self.parse_product(page, parent)
        elif len(selects) == 2:
            quantity_select, type_select = selects
            quantity_select_selector = f'select[name="{quantity_select}"]'
            type_select_selector = f'select[name="{type_select}"]'
            quantity_options = response.css(f'{quantity_select_selector} option::attr(value)').getall()
            type_options = response.css(f'{type_select_selector} option::attr(value)').getall()
            for quantity in quantity_options:
                for type in type_options:
                    page = self.multi_select(response.url, [quantity_select_selector, type_select_selector], [quantity, type], .5, 'a.cpnb-accept-btn')
                    yield self.parse_product(page, parent)

    def parse_product(self, page, parent):
        i = ItemLoader(item=Product(), selector=page)

        # General info
        i.context['prefix'] = 'VP'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        if not page.css('span.sku').get():
            print('    DEBUG NO SKU')
        i.add_css('id', 'span.sku')
        i.add_css('sid', 'span.sku')
        i.add_value('parent', parent)

        selections = page.css('option[selected=selected]::text').getall()
        selected_quantity = None
        selected_type = None
        if len(selections) == 1:
            selected_quantity = page.css('option[selected=selected]::text').getall()
        elif len(selections) == 2:
            selected_quantity, selected_type = page.css('option[selected=selected]::text').getall()
        i.add_value('size', selected_quantity)
        title = page.css('h1.product-title').get()
        i.add_value('title', f'{title} ({selected_type})')
        i.add_css('price', 'div.sale-price')

        # # Descriptions
        # desc_selector = 'div.gf_restabs > div.item-content'
        # desc_tabs = response.css('ul > li.gf_tab div.elm::text').getall()
        # desc_tabs_size = len(desc_tabs)
        # if desc_tabs_size == 0:
        #     desc_tabs = response.css("div.module > div > div.chevron div.elm > p > b::text").getall()
        #     desc_tabs_size = len(desc_tabs)
        #     desc_selector = 'article.item-content div.element-wrap div.elm.text-edit.gf-elm-left.gf-elm-left-lg.gf-elm-left-md.gf-elm-left-sm.gf-elm-left-xs.gf_gs-text-paragraph-1'
        # desc_tabs = list(filter(lambda tab: tab not in ["So gefällt es unseren Kunden", "Bewertungen"], desc_tabs))
        # for n in range(desc_tabs_size - 1):
        #     if n == 6: break
        #     i.add_value(f'title_{n+1}', desc_tabs[n])
        #     i.add_css(f'content_{n+1}', f'{desc_selector}:nth-of-type({n+1})')
        #     i.add_css(f'content_{n+1}_html', f'{desc_selector}:nth-of-type({n+1})')

        # # Product images
        # for img in response.css('div.gf_product-images-list > a > div.gf_product-image-thumb > img::attr(src)').getall():
        #     i.add_value('image_urls', response.urljoin(img))

        return i.load_item()
