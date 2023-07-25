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
                    page = self.select_click(response.url,
                                             quantity_select_selector,
                                             quantity,
                                             'select[name*="product_option"]',
                                             .5,
                                             'a.cpnb-accept-btn')
                    yield self.parse_product(page=page,
                                             parent=parent,
                                             selections=[page.css(f'option[value="{quantity}"]::text').get()])
        elif len(selects) == 2:
            quantity_select, type_select = selects
            quantity_select_selector = f'select[name="{quantity_select}"]'
            type_select_selector = f'select[name="{type_select}"]'
            quantity_options = response.css(f'{quantity_select_selector} option::attr(value)').getall()
            type_options = response.css(f'{type_select_selector} option::attr(value)').getall()
            for quantity in quantity_options:
                for type in type_options:
                    page = self.multi_select_click(response.url,
                                                   [quantity_select_selector, type_select_selector],
                                                   [quantity, type],
                                                   'select[name*="product_option"]',
                                                   .5,
                                                   'a.cpnb-accept-btn')
                    yield self.parse_product(page=page,
                                             parent=parent,
                                             selections=[page.css(f'option[value="{quantity}"]::text').get(), page.css(f'option[value="{type}"]::text').get()])

    def parse_product(self, page, parent, selections):
        i = ItemLoader(item=Product(), selector=page)

        # General info
        i.context['prefix'] = 'VP'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        i.add_css('id', 'span.sku')
        i.add_css('sid', 'span.sku')
        i.add_value('parent', parent)

        selected_quantity = None
        selected_type = None
        if len(selections) == 1:
            selected_quantity = selections[0]
        elif len(selections) == 2:
            selected_quantity, selected_type = selections
        i.add_value('size', selected_quantity)
        title = page.css('h1.product-title').get()
        i.add_value('title', f'{title} ({selected_type})' if selected_type else title)
        i.add_css('price', 'div.sale-price')

        # Descriptions
        ignored_titles = ['Produktdetails', False, None]
        desc_titles = page.css('div.product-ldesc h5::text').getall()
        skipped = 0
        for n in range(len(desc_titles)):
            if n+1-skipped >= 7:
                break
            if desc_titles[n] in ignored_titles:
                skipped += 1
                continue
            i.add_value(f'title_{n+1-skipped}', desc_titles[n])
            i.add_value(f'content_{n+1-skipped}', page.css(f'div.product-ldesc h5 + *').getall()[n])
            i.add_value(f'content_{n+1-skipped}_html', page.css(f'div.product-ldesc h5 + *').getall()[n])

        # Product images
        i.add_css('image_urls', 'img.j2store-product-main-image::attr(src)')

        return i.load_item()
