from abc import ABC, abstractmethod

from selenium.webdriver.chromium.webdriver import ChromiumDriver

class Handler(ABC):
  def __init__(self, driver: ChromiumDriver) -> None:
    self.driver = driver
    
  @abstractmethod
  def url(self):
      pass

  @abstractmethod
  def handle(self):
     pass
