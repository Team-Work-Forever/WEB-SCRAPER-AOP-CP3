from handler.buy_house_handler import BuyHouseHandler
from handler.era_handler import EraHandler
from handler.remax_handler import RemaxHandler
from scraper import Scraper, webdriver

if __name__ == "__main__":
  options = webdriver.EdgeOptions()
  options.add_argument("--enable-chrome-browser-cloud-management")
  options.add_argument('--remote-debugging-pipe')
  options.add_argument('--disable-notifications')
  options.add_argument("--no-sandbox")
  options.add_experimental_option("detach", True)

  driver_path = r"driver\msedgedriver.exe"

  scraper = Scraper(
    driver_path,
    [
      EraHandler,
      BuyHouseHandler,
      RemaxHandler,
    ],
    options
  )

  scraper.start_scraping("results.csv")