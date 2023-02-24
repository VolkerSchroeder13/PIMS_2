import json
from scrapy.loader import ItemLoader
from scrapy import FormRequest, Spider, Request
from PIMS.items import Product


class AtcomSpider(Spider):

    name = 'atcom'
    allowed_domains = ['atcomhorse.de']
    start_urls = ['https://www.atcomhorse.de/p/atcom-arthro-sport/584260']

    def parse(self, response):
        yield FormRequest(
            url="https://www.atcomhorse.de/detail/caa87d4b43c44bb788d9d323b02d3c3e/switch",
            formdata={
                "options": "%7B%223f84f4a1f9cf42bf960b85c3937ffff5%22%3A%22aaf54fa88dc6431da54d50b08b91130f%22%7D",
                "switched": "3f84f4a1f9cf42bf960b85c3937ffff5"
            },
            method='GET',
            callback=self.parse_test
        )
   
    def parse_test(self, response):
        yield Request(url=json.loads(response.text)['url'], callback=self.test)

    def test(self, response):
        print(response.css('span.product-detail-ordernumber::text').get())