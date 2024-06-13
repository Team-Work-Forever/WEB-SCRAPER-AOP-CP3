from selenium.webdriver.chromium.webdriver import ChromiumDriver
from contracts.locationResult import LocationResult
from contracts.offerResult import OfferResult
from contracts.propertyDetailsResult import PropertyDetailsResult
from contracts.propertyResult import PropertyResult
from contracts.urlResult import UrlResult
from handler.handler import Handler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

class RemaxHandler(Handler):
  cookies_btn = ".//button[@class='cookies-button' and @id='rcc-confirm-button']"
  number_pages_text = ".//h1[@class='total-results-text']"
  next_page_button = ".//a[@class='page-link' and @role='button']"
  first_page = 1
  number_card_per_page = 20
  labels = ["comprar", "arrendar"]


  def __init__(self, driver: ChromiumDriver) -> None:
    super().__init__(driver)

  def url(self, page: int, type: str):
    # return f"https://www.remax.pt/{type}?searchQueryState=%7B%22regionName%22:%22%22,%22sort%22:%7B%22fieldToSort%22:%22PublishDate%22,%22order%22:1%7D,%22businessType%22:1,%22page%22:{page},%22t%22:%22%22,%22mapIsOpen%22:false,%22mapScroll%22:false,%22searchNextToMe%22:false,%22publishDate%22:30%7D"
    return f"https://www.remax.pt/{type}?searchQueryState=%7B%22regionName%22:%22%22,%22businessType%22:2,%22page%22:{page},%22sort%22:%7B%22fieldToSort%22:%22PublishDate%22,%22order%22:1%7D%7D"

  def handle(self):
    properties = [PropertyResult]

    self.driver.get(self.url(self.first_page, self.labels[0]))

    self.wait_and_click(By.XPATH, self.cookies_btn)

    for label in self.labels:

      number_pages_text_elem = self.wait_and_find(By.XPATH, self.number_pages_text).text
      number_pages_parts = number_pages_text_elem.split(' ', 1)
      number_pages = int(int(number_pages_parts[0].replace(".", "").strip()) / int(self.number_card_per_page))
      number_pages = 1

      for i in range(self.first_page, number_pages + 1):
        self.driver.get(self.url(i, label))
        
        cards_collection = self.wait_and_find(By.XPATH, ".//div[@class='row results-list ']")
        cards = cards_collection.find_elements(By.XPATH, ".//div[@class='col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3 result']//div[@class='listing-search-searchdetails-component' and contains(@id, 'listing-search-searchdetails-component-')]")

        for card in cards:
          details = {}
         
          # Url
          card_url_element = self.wait_and_find_in_elem(card, By.XPATH, ".//a")
          card_url = card_url_element.get_attribute('href')

          # Location
          card_location = self.wait_and_find_in_elem(card, By.XPATH, ".//h2[@class='listing-address']").text
          card_district_parts = card_location.split('-', 1)
          card_location = card_district_parts[1].strip() + ", " + card_district_parts[0]

          # Price and Type of offer
          card_type = label
          card_price = self.wait_and_find_in_elem(card,By.XPATH, ".//p[@class='listing-price']").text

          # Info house
          card_property_details_collection = self.wait_and_find_in_elem(card,By.XPATH, ".//ul[@class='listing-footer']")
          card_property_details = card_property_details_collection.find_elements(By.XPATH, ".//li[contains(@class, 'listing-')]")

          for detail in card_property_details:
            if detail.get_attribute("class") == 'listing-type':
              card_property_type = self.wait_and_find_in_elem(card,By.XPATH, ".//li[@class='listing-type']").text
            else:
              detail_key_element = self.wait_and_find_in_elem(detail, By.XPATH, ".//i[contains(@class, 'icon-')]")
              detail_key = detail_key_element.get_attribute('class')
              detail_value = detail.text
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