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

            content = page.content()
            page.close

            return Selector(text=content)
    
    def select(self, url, select, option, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(url)
            page.select_option(selector=select, value=option)
            
            sleep(delay)

            content = page.content()
            page.close()
            
            return Selector(text=content)
        
    def click(self, url, buttons, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(url)
            
            for button in buttons:
                page.get_by_role('button').get_by_text(button).click()
                sleep(delay)
                
            content = page.content()
            page.close()

            return Selector(text=content)
        
    def click(self, url, selector, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            page.goto(url)

            pages = []
           
            for button in page.locator(selector=selector).all():
                button.click()
                pages.append(Selector(text=page.content()))
                sleep(delay)
                
            page.close()

            return pages
        