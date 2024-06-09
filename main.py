from scraper import Scraper, webdriver

from handler.imo_virtual_handler import ImoVirtualHandler

options = webdriver.EdgeOptions()
options.add_argument("--enable-chrome-browser-cloud-management")
options.add_argument('--remote-debugging-pipe')
options.add_argument('--disable-notifications')
options.add_argument("--no-sandbox")
options.add_experimental_option("detach", True)

scraper = Scraper(
  "driver\msedgedriver.exe",
  [
    ImoVirtualHandler
  ],
  options
)

scraper.start_scraping()