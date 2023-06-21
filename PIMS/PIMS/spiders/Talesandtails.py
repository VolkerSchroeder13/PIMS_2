from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
from time import sleep
import json


class TalesandtailsSpider(BaseSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": "2.5",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    name = 'Talesandtails'
    address = '7028700'
    allowed_domains = ['talesandtails.de']
    start_urls = ['https://talesandtails.de/collections/']

    visited_products = []
    visited_variations = []

    def search_json_item(self, contained_str, page, script_selector = 'script.product-json::text'):
        json_item = None
        for script in page.css(script_selector).getall():
            if contained_str in script:
                json_item = json.loads(script)
        return json_item

    def parse(self, response):
        for href in response.css('a.collection-grid-item__link::attr(href)').getall():
            if(href == '#'):
                continue
            yield Request(url=response.urljoin(href), callback=self.parse_pages)

    def parse_pages(self, response):
        page_count = response.css('div#Collection > ul.pagination > li:nth-of-type(2)::text').get()
        if page_count == None:
            page_count = 1
        else:
            page_count = int(page_count.replace(' ', '').split('von')[-1][0])

        for n in range(page_count):
            yield Request(url=f'{response.url}?page={n+1}', callback=self.parse_category)


    def parse_category(self, response):
        urls = []
        for href in response.css('a.grid-view-item__link::attr(href)').getall():
            urls.append(response.urljoin(href))
        urls = list(filter(lambda url: url not in self.visited_products, urls))
        self.visited_products.extend(urls)
        for url in urls:
            yield Request(url=url, callback=self.parse_variation)


    def parse_variation(self, response):
        title = response.css("span.gf_product-title::text").get()
        json = self.search_json_item(f'"title":"{title}"', response)
        if json == None: return

        root = json['variants'][0]['sku']
        if len(root) > 4:
            root = json['variants'][0]['barcode']

        vars = []
        for var in json['variants']:
            vars.append(str(var['id']))
        vars = list(filter(lambda var: var not in self.visited_variations, vars))
        self.visited_variations.extend(vars)
        for var in vars:
            yield Request(
                url=(response.url+'?variant='+var),
                callback=self.parse_product,
                cb_kwargs=dict(parent=root, variation=var)
            )


    def parse_product(self, response, parent, variation):
        title = response.css("span.gf_product-title::text").get()
        json = self.search_json_item(f'"title":"{title}"', response)
        if json == None: return

        i = ItemLoader(item=Product(), selector=response)

        # General info
        i.context['prefix'] = 'TL'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        for var in json['variants']:
            if str(var['id']) != variation: continue

            sku = var['sku']
            if len(sku) > 4:
                sku = var['barcode']
            if sku == None or sku == "":
                return
            i.add_value('id', sku)
            i.add_value('sid', sku)

            if var['title'] != "Default Title":
                i.add_value('size', var['title'])
            break
        i.add_value('parent', parent)
        i.add_value('title', title)
        i.add_css('price', 'span.gf_product-price.money.gf_gs-text-paragraph-1')

        # Descriptions
        desc_selector = 'div.gf_restabs > div.item-content'
        desc_tabs = response.css('ul > li.gf_tab div.elm::text').getall()
        desc_tabs_size = len(desc_tabs)
        if desc_tabs_size == 0:
            desc_tabs = response.css("div.module > div > div.chevron div.elm > p > b::text").getall()
            desc_tabs_size = len(desc_tabs)
            desc_selector = 'article.item-content div.element-wrap div.elm.text-edit.gf-elm-left.gf-elm-left-lg.gf-elm-left-md.gf-elm-left-sm.gf-elm-left-xs.gf_gs-text-paragraph-1'
        desc_tabs = list(filter(lambda tab: tab not in ["So gefällt es unseren Kunden", "Bewertungen"], desc_tabs))
        for n in range(desc_tabs_size - 1):
            if n == 6: break
            i.add_value(f'title_{n+1}', desc_tabs[n])
            i.add_css(f'content_{n+1}', f'{desc_selector}:nth-of-type({n+1})')
            i.add_css(f'content_{n+1}_html', f'{desc_selector}:nth-of-type({n+1})')

        # Product images
        for img in response.css('div.gf_product-images-list > a img::attr(src)').getall():
            i.add_value('image_urls', response.urljoin(img))

        yield i.load_item()
