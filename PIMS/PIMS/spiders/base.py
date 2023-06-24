from playwright.sync_api import sync_playwright
from scrapy import Spider, Selector
from time import sleep


class BaseSpider(Spider):

    def __init__(self):
        super().__init__()

    def page(self, url, delay = None):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            if delay: sleep(delay)

            content = page.content()
            page.close

            return Selector(text=content)

    def page_scroll_down(self, url, delay, cookies=None):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            if cookies is not None:
                page.locator(selector=cookies).click()
                sleep(delay)

            for i in range(5):
                page.mouse.wheel(0, 100000)
                sleep(delay)

            content = page.content()
            page.close()

            return Selector(text=content)

    def select(self, url, select, option, delay, cookies=None):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            if cookies is not None:
                page.locator(selector=cookies).click()
                sleep(delay)

            page.select_option(selector=select, value=option)
            sleep(delay)

            content = page.content()
            page.close()

            return Selector(text=content)

    def click(self, url, selector, delay, cookies=None):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            if cookies is not None:
                page.locator(selector=cookies).click()
                sleep(delay)

            pages = []

            for button in page.locator(selector=selector).all():
                button.click()
                pages.append(Selector(text=page.content()))
                sleep(delay)

            page.close()

            return pages

    def page_hover(self, url, selector, delay = None):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            if delay: sleep(delay)

            page.hover(selector=selector)

            sleep(delay/2) if delay else sleep(.5)

            content = page.content()
            page.close

            return Selector(text=content)
