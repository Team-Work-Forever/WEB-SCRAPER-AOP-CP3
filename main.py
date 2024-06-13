from handler.buy_house_handler import BuyHouseHandler
from handler.era_handler import EraHandler
from handler.remax_handler import RemaxHandler
from handler.imo_virtual_handler import ImoVirtualHandler
from scraper import Scraper, webdriver

options = webdriver.EdgeOptions()
options.add_argument("--enable-chrome-browser-cloud-management")
options.add_argument('--remote-debugging-pipe')
options.add_argument('--disable-notifications')
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)

scraper = Scraper(
  "driver\msedgedriver.exe",
  [
    # ImoVirtualHandler
    # EraHandler
    # BuyHouseHandler
    RemaxHandler
  ],
  options
)

scraper.start_scraping()