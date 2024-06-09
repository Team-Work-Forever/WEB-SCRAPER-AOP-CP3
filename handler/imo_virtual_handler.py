from selenium.webdriver.chromium.webdriver import ChromiumDriver
from handler.handler import Handler

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class ImoVirtualHandler(Handler):
  cookies_btn = '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[1]'
  house_type_xpath = '/html/body/div[1]/div[2]/main/div/div[2]/div[1]/div/form/div[1]/div[1]/div[1]/div/div/div/div[1]/div'

  def __init__(self, driver: ChromiumDriver) -> None:
    super().__init__(driver)

  def url(self):
    return "https://www.imovirtual.com/pt/resultados/comprar/apartamento/todo-o-pais?viewType=listing&limit=72"
  
  def find_combox(self) -> Select:
    return self.driver.find_element(by=By.XPATH, value=self.house_type_xpath)

  def wait_and_find(self, by: By, path: str):
    return WebDriverWait(self.driver, 15).until(
        EC.presence_of_element_located((by, path))
    )

  def handle(self):
    self.driver.get(self.url())

    element = self.wait_and_find(By.ID, "onetrust-accept-btn-handler")
    element.click()

    house_input = self.wait_and_find(By.XPATH, self.house_type_xpath)
    house_input.click()

    # combox = self.find_combox()
    # combox.click()

    # options = combox.options

    # print(options)

    ActionChains(self.driver).pause(seconds=5000)