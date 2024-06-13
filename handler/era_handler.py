from selenium.webdriver.chromium.webdriver import ChromiumDriver
from contracts.locationResult import LocationResult
from contracts.offerResult import OfferResult
from contracts.propertyDetailsResult import PropertyDetailsResult
from contracts.propertyResult import PropertyResult
from contracts.urlResult import UrlResult
from handler.handler import Handler

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

class EraHandler(Handler):
  cookies_btn = ".//button[@class='ml-2 btn btn-primary btn-sm']"
  number_pages_button = ".//button[@class='btn-page btn-page-lg']"
  first_page = 0


  def __init__(self, driver: ChromiumDriver) -> None:
    super().__init__(driver)

  def url(self, page: int):
    return f"https://www.era.pt/comprar?ob=1,2&tp=1,2&page={page}&ord=3"

  def handle(self):
    properties = [PropertyResult]

    self.driver.get(self.url(self.first_page))

    self.wait_and_click(By.XPATH, self.cookies_btn)

    number_pages = int(self.wait_and_find(By.XPATH, self.number_pages_button).text) 
    number_pages = 2


    for i in range(self.first_page, number_pages):
      self.driver.get(self.url(i))
      
      cards_collection = self.wait_and_find(By.XPATH, ".//div[@class='row cards-container']")
      cards = cards_collection.find_elements(By.XPATH, ".//div[@class='card col-12 col-md-6 col-lg-4 ']")

      for card in cards:
        details = {}

        # Url
        card_url_element = card.find_element(By.XPATH, ".//a[@class='card-anchor']")
        card_url = card_url_element.get_attribute('href')

        # Location
        card_location = card.find_element(By.XPATH, ".//div[@class='col-12 location']").text

        # Price and Type of offer
        card_type = card.find_element(By.XPATH, ".//p[@class='price-label d-block m-0']").text
        card_price = card.find_element(By.XPATH, ".//p[@class='price-value']").text
        
        # Info house
        card_property_type = card.find_element(By.XPATH, ".//p[@class='property-type d-block mb-1']").text
        card_property_details_collection = card.find_element(By.XPATH, ".//div[@class='property-details mb-3']")
        card_property_details = card_property_details_collection.find_elements(By.XPATH, ".//div[@class='detail d-inline-flex mr-2']")

        for detail in card_property_details:
          detail_key_element = detail.find_element(By.XPATH, ".//*[name()='svg' and @class='icon' and @data-toggle='tooltip']")
          detail_key = detail_key_element.get_attribute("data-original-title")
          detail_value = detail.find_element(By.XPATH, ".//span[@class='d-inline-flex ']").text
          details[detail_key] = detail_value

        properties.append(PropertyResult(
          url=UrlResult(url=card_url),
          location=LocationResult(location=card_location),
          offer=OfferResult(price=card_price, typeOffer=card_type),
          property_details=PropertyDetailsResult(type=card_property_type, details=details)
        ))

      i += i

    ActionChains(self.driver).pause(seconds=500)
    return properties