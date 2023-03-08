from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
from dotenv import dotenv_values
from scrapy import Spider
from time import sleep
import logging


class BaseSpider(Spider):

    def __init__(self):
        super().__init__()

        self.config = dotenv_values("../../.env")

        self.options = Options()
        self.options.add_argument("--headless=new")
        
        self.driver = Edge(
            executable_path=self.config.get('DRIVER'), 
            options=self.options
        )

        logging.getLogger('selenium').setLevel(logging.WARNING)

    def get_page(self, url, select, option):
        self.driver.get(url)
        
        page = Select(self.driver.find_element(By.CSS_SELECTOR, select))
        page.select_by_value(option)
        
        sleep(5)

        return self.driver.current_url
       
