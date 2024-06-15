import csv

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

  def result_to_dict(self, result):
      details = result.property_details.details

      result_data = {
          "url": result.url.url,
          "location": result.location.location,
          "district": result.location.district,
          "price": result.offer.price,
          "currency": result.offer.currency,
          "offer_type": result.offer.typeOffer,
          "property_type": result.property_details.type,
          "area": details.get(1, 0),
          "landArea": details.get(2, 0),
          "privateArea": details.get(3, 0),
          "bathRooms": details.get(4, 0),
          "bedRooms": details.get(5, 0),
          "parking": details.get(6, 0),
          "floors": details.get(7, 0),
          "energeticCertificate": details.get(8, 0),
          "lift": details.get(9, 0),
          "fenced": details.get(10, 0),
          "fractions": details.get(11, 0),
      }
      return result_data


  def start_scraping(self, output_csv: str):

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
      fieldnames = [
          "url",
          "location",
          "district",
          "price",
          "currency",
          "offer_type",
          "property_type",
          "area",
          "landArea",
          "privateArea",
          "bathRooms",
          "bedRooms",
          "parking",
          "floors",
          "energeticCertificate",
          "lift",
          "fenced",
          "fractions",
      ]

      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()

      for web_site in self.websites_url:
        handler = web_site(self.driver)
        for result in handler.handle():
          result_data = self.result_to_dict(result)
          writer.writerow(result_data)