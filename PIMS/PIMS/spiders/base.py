from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
from dotenv import dotenv_values
from scrapy import Spider


class BaseSpider(Spider):

    def __init__(self):
        super().__init__()
        self.config = dotenv_values("../../.env")
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.driver = Edge(executable_path=self.config.get('DRIVER'), options=self.options)

    def get_page(self, url, select, option):
        self.driver.get(url)

        try:
            sel = Select(self.driver.find_element(By.CSS_SELECTOR, select))
            sel.select_by_value(option)
            self.driver.implicitly_wait(5)
            return Select(self.driver.page_source)
        except: pass