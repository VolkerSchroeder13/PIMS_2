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

    # scroll down page to load content/pages that only get revealed by scrolling down
    # ! made for and only tested for sanadog.com (for now)
    # * still might not be 100% reliable because of inconsistent page behavior
    def page_scroll_down(self, url, delay):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            sleep(delay)

            for i in range(5):
                # scroll down to bottom of page
                page.mouse.wheel(0, 15000)
                sleep(.5)
                # scroll up a bit
                page.mouse.wheel(0, -2000)
                # scroll back down gradually to make sure stuff actually loads
                for _ in range(10):
                    sleep(.5)
                    page.mouse.wheel(0, 200)
                i += 1

            sleep(delay / 2)

            content = page.content()

            page.close()
            browser.close()

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
