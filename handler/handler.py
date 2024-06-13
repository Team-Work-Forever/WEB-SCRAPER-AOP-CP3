from abc import ABC, abstractmethod

from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

class Handler(ABC):
  def __init__(self, driver: ChromiumDriver) -> None:
    self.driver = driver
    
  @abstractmethod
  def url(self):
      pass

  def wait_and_find(self, by: By, path: str) -> WebElement:
    return WebDriverWait(self.driver, 15).until(
      EC.presence_of_element_located((by, path))
    )

  def wait_and_find_in_elem(self, elem, by: By, path: str) -> WebElement:
    return WebDriverWait(elem, 15).until(
      EC.presence_of_element_located((by, path))
    )
  
  def wait_and_click(self, by: By, path: str):
    element = self.wait_and_find(by, path)
    WebDriverWait(self.driver, 15).until(
        EC.element_to_be_clickable((by, path))
    )
    element.click()

  @abstractmethod
  def handle(self):
     pass
