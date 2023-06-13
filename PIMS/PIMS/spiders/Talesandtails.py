from scrapy.loader import ItemLoader
from PIMS.spiders.base import BaseSpider
from scrapy import Spider, Request
from PIMS.items import Product
from time import sleep
import json


class SanadogSpider(BaseSpider):
    custom_settings = {
        "DOWNLOAD_DELAY": "2",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    name = 'TalesandTails'
    address = '7028700'
    allowed_domains = ['talesandtails.de']
    start_urls = ['https://talesandtails.de/collections/']

    def parse(self, response):
        for href in response.css('a.collection-grid-item__link::attr(href)').getall():
            if(href == '#'):
                continue
            print(f"    DEBUG: category {href}")
            # print(f'    DEBUG: {len(response.css("haahhaha").getall())}')
            yield Request(url=response.urljoin(href), callback=self.parse_category)

    def parse_category(self, response):
        for href in response.css('a.grid-view-item__link::attr(href)').getall():
            print(f'    DEBUG: product {href}')
            yield Request(url=response.urljoin(href), callback=self.parse_variation)

    def parse_variation(self, response):
        json_item = None
        title = response.css("span.gf_product-title::text").get()
        for script in response.css('script.product-json::text').getall():
            if f'"title":"{title}"' in script:
                json_item = json.loads(script)
        if json_item == None:
            return
        root = json_item['variants'][0]['sku']
        if len(root) > 4:
            root = json_item['variants'][0]['barcode']
        vars = []
        for var in json_item['variants']:
            vars.append(str(var['id']))
        print(f"    DEBUG: vars {vars}")
        # vars.append('')
        for var in vars:
            yield Request(
                url=(response.url+'?variant='+var),
                callback=self.parse_product,
                cb_kwargs=dict(parent=root, variation=var)
            )


    def parse_product(self, response, parent, variation):
        print(f"    DEBUG: product {response.url}")
        json_item = None
        title = response.css("span.gf_product-title::text").get()
        for script in response.css('script.product-json::text').getall():
            if f'"title":"{title}"' in script:
                json_item = json.loads(script)
                break
        if json_item == None:
            return
        i = ItemLoader(item=Product(), selector=response)

        i.context['prefix'] = 'TL'
        i.add_value('address', self.address)
        i.add_value('brand', self.name)
        for var in json_item['variants']:
            print(f"    DEBUG: vari {variation}")
            print(f"    DEBUG: id {var['id']}")
            if str(var['id']) != variation:
                continue
            sku = var['sku']
            if len(sku) > 4:
                sku = var['barcode']
            if sku == None or sku == "":
                return
            print(f"    DEBUG: sku {sku}")
            i.add_value('id', sku)
            i.add_value('sid', sku)
            if var['title'] != "Default Title":
                i.add_value('size', var['title'])
            break
        i.add_value('parent', parent)
        i.add_value('title', title)
        i.add_css('price', 'span.gf_product-price.money.gf_gs-text-paragraph-1')

        # size = response.css('span.gf_swatch.gf_selected::attr(data-value)').get()
        # if size != None:
        #     i.add_value('size', size.split('(')[0])

        # TODO? selector
        # for item in response.css('script[type="application/ld+json"]::text').getall():
        #     selector = ""
        #     if '"@type": "BreadcrumbList"' in item:
        #         json_item = json.loads(item)
        #         for n in range(len(json_item['itemListElement']) - 1):
        #             if n != 0:
        #                 selector += " "
        #             selector += json_item['itemListElement'][n]['name']
        #         i.add_value('selector', selector)

        desc_tabs = response.css('ul > li.gf_tab div.elm::text').getall()
        if len(desc_tabs) > 0 and desc_tabs[-1] in ["So gefällt es unseren Kunden", "Bewertungen"]:
            desc_tabs.pop()
        descs = response.css('div.gf_restabs > div.item-content::text').getall()
        for n in range(len(desc_tabs)):
            if n == 6:
                break
            i.add_value(f'title_{n+1}', desc_tabs[n])
            i.add_css(f'content_{n+1}', f'div.gf_restabs > div.item-content:nth-of-type({n+1})')
            i.add_css(f'content_{n+1}_html', f'div.gf_restabs > div.item-content:nth-of-type({n+1})')
        print(f"    DEBUG: tabs {desc_tabs}")
        if len(desc_tabs) == 0:
            desc_tabs = response.css("div.module > div > div.chevron div.elm > p > b::text").getall()
            if len(desc_tabs) > 0 and desc_tabs[-1] in ["So gefällt es unseren Kunden", "Bewertungen"]:
                desc_tabs.pop()
            descs = response.css('article.item-content div.element-wrap div.elm.text-edit.gf-elm-left.gf-elm-left-lg.gf-elm-left-md.gf-elm-left-sm.gf-elm-left-xs.gf_gs-text-paragraph-1::text').getall()
            for n in range(len(desc_tabs)):
                if n == 6:
                    break
                i.add_value(f'title_{n+1}', desc_tabs[n])
                i.add_css(f'content_{n+1}', f'article.item-content div.element-wrap div.elm.text-edit.gf-elm-left.gf-elm-left-lg.gf-elm-left-md.gf-elm-left-sm.gf-elm-left-xs.gf_gs-text-paragraph-1:nth-of-type({n+1})')
                i.add_css(f'content_{n+1}_html', f'article.item-content div.element-wrap div.elm.text-edit.gf-elm-left.gf-elm-left-lg.gf-elm-left-md.gf-elm-left-sm.gf-elm-left-xs.gf_gs-text-paragraph-1:nth-of-type({n+1})')
            print(f"    DEBUG: tabs {desc_tabs}")

        for img in response.css('div.gf_product-images-list > a > div.gf_product-image-thumb > img::attr(src)').getall():
            i.add_value('image_urls', response.urljoin(img))

        yield i.load_item()
