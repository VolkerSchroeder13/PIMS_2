from playwright.sync_api import sync_playwright
from scrapy import Spider, Selector


class BaseSpider(Spider):

    def __init__(self):
        super().__init__()
 
    def next(self, url, select, option):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.select_option(selector=select, value=option)
            return Selector(text=page.content())