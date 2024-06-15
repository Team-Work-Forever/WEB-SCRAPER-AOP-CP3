from selenium.webdriver.chromium.webdriver import ChromiumDriver
from contracts.locationResult import LocationResult
from contracts.offerResult import OfferResult
from contracts.propertyDetailsResult import PropertyDetailsResult
from contracts.propertyResult import PropertyResult
from contracts.urlResult import UrlResult
from handler.handler import Handler

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By

class BuyHouseHandler(Handler):
  cookies_btn = ".//button[@id='onetrust-accept-btn-handler']"
  number_pages_text = ".//span[@class='pagination_middleText']"
  first_page = 0

  def __init__(self, driver: ChromiumDriver) -> None:
    super().__init__(driver)

  def url(self, page: int):
    return f"https://www.comprarcasa.pt/imoveis?p={page}&ltype=1&orderby=0&el=32"

  def handle(self):
    self.driver.get(self.url(self.first_page))

    self.wait_and_click(By.XPATH, self.cookies_btn)

    number_pages_text_elem = self.wait_and_find(By.XPATH, self.number_pages_text).text
    number_pages_parts = number_pages_text_elem.rsplit(' ', 1)
    number_pages = int(number_pages_parts[1].strip())

    for i in range(self.first_page, number_pages):
      self.driver.get(self.url(i))
      
      cards_collection = self.wait_and_find(By.XPATH, ".//ul[@class='gridList']")
      cards = cards_collection.find_elements(By.XPATH, ".//a[@class='prop ']")

      for card in cards:
        try:
          details = {}

          # Url
          card_url = card.get_attribute('href')

          # Location
          card_location = card.find_element(By.XPATH, ".//h3[@class='prop_subTitle']").text

          # Price and Type of offer
          card_type = card.find_element(By.XPATH, ".//span[@class='stamp stamp--primary']").text
          
          card_price = ''

          try:
            haveReducedPrice = card.find_element(By.XPATH, ".//span[@class='reduzedPriceItemSymbol']").text
            if haveReducedPrice:
                card_price = self.wait_and_find_in_elem(card, By.XPATH, ".//span[@class='prop_tag']").text
                card_price = card_price.split('€', 1)[1].strip()

          except NoSuchElementException:
            pass
          
          if not card_price:
            card_price = self.wait_and_find_in_elem(card, By.XPATH, ".//span[@class='prop_tag']").text

          # Info house
          card_property_type = card.find_element(By.XPATH, ".//h2[@class='prop_title']").text
          card_property_details_collection = card.find_element(By.XPATH, ".//ul[@class='prop_details']")
          card_property_details = card_property_details_collection.find_elements(By.XPATH, ".//li")

          for detail in card_property_details:
            detail_key_element = detail.find_element(By.XPATH, ".//i")
            detail_key = detail_key_element.get_attribute("class")
            detail_value = detail.text
            details[detail_key] = detail_value

          yield PropertyResult(
            url=UrlResult(url=card_url),
            location=LocationResult(location=card_location),
            offer=OfferResult(price=card_price, typeOffer=card_type),
            property_details=PropertyDetailsResult(type=card_property_type, details=details)
          )
          
        except Exception:
          print("Card without description!")
          pass

      i += 1