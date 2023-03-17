from playwright.sync_api import sync_playwright
from scrapy import Spider, Selector
from time import sleep


class BaseSpider(Spider):

    def __init__(self):
        super().__init__()
 
    def page(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            return Selector(text=page.content())
    
    def variation(self, url, select, option, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.select_option(selector=select, value=option)
            sleep(delay)
            return Selector(text=page.content())