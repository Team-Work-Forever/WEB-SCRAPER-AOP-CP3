from selenium import webdriver 

from selenium.webdriver.chromium import service as driver_service
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.webdriver import ChromiumDriver

from handler.handler import Handler

class Scraper():
  driver: ChromiumDriver
  service: driver_service

  def __init__(self, driver_path: str, websites: list[Handler], options: ChromiumOptions = None):
    self.websites_url = websites
    self.service = webdriver.EdgeService(executable_path=driver_path)
    self.driver = webdriver.Edge(service=self.service, options=options)
    self.driver.maximize_window()

  def get_driver(self) -> ChromiumDriver: 
    return self.driver

  def start_scraping(self):
    for web_site in self.websites_url:
      handler = web_site(self.driver)
      result = handler.handle()
      for r in result:
        print(r)