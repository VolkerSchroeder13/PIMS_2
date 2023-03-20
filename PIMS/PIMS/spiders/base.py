from playwright.sync_api import sync_playwright
from scrapy import Spider, Selector
from time import sleep


class BaseSpider(Spider):

    def __init__(self):
        super().__init__()
 
    def page(self, url, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(url)
            sleep(delay)
            page.close

            return Selector(text=page.content())
    
    def select(self, url, select, option, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(url)
            page.select_option(selector=select, value=option)
            
            sleep(delay)
            page.close()
            
            return Selector(text=page.content())
        
    def click(self, url, buttons, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(url)
            
            for button in buttons:
                page.get_by_text(button, exact=True).click()
                sleep(delay)
                
            page.close()

            return Selector(text=page.content())