import time

from YellowPages1 import YellowPages1 
from YellowPages2 import YellowPages2
from GoogleMapScraper import GoogleMapScraper
from LinkedInScraper import LinkedInScraper
from Madayp import Madayp
from GemScraper import GemScraper

def mainFunction():
    keywords = ['transportation', 'construction', 'furniture', 'office', 
                        'school supplies', 'material', 'concrete', 'mud brick', 
                        'thatched roofing', 'truck', 'freight', 'train', 'utility', 
                        'electricity', 'sewage','building materials', 'hardware', 
                        'wood', 'roofs','solar panel', 'water tank','crane','plumbing',
                        'artisan','hotel','taxi']
    
    # Choose chromedriver appropriate for system
    # may also need to add executable permission for the file

    # chrome_driver_path='chromedriver-mac.exe'
    chrome_driver_path='chromedriver.exe'
    
    # scraper api key
    api_key = 'INSERT SCRAPERAPI KEY HERE'

    # Some scrapers take a long time to run, may only want to run one scraper at a time.
    yellow_pages1 = YellowPages1(keywords)
    yellow_pages1.parse() 
    yellow_pages1.append_data_to_csv()

    yellow_pages2 = YellowPages2(keywords,chrome_driver_path=chrome_driver_path)
    yellow_pages2.parse()
    yellow_pages2.append_data_to_csv()

    google_map_scraper = GoogleMapScraper(keywords,chrome_driver_path=chrome_driver_path,wait_time=5)
    google_map_scraper.get_business_urls()
    google_map_scraper.parse()
    google_map_scraper.append_data_to_csv()

    linked_in_scraper = LinkedInScraper(keywords)
    linked_in_scraper.addExtension()
    linked_in_scraper.loginToLinkedIn()
    time.sleep(5)
    linked_in_scraper.creatingBusinessList()
    linked_in_scraper.append_data_to_csv()

    madayp_scraper = Madayp(api_key=api_key)
    madayp_scraper.parse()
    madayp_scraper.append_data_to_csv()

    gem_scraper = GemScraper('')
    # Grabs all business URLs
    gem_scraper.parse()
    # Parse each individual business page
    gem_scraper.parseBusinessPages()
    # Return list of businesses and their info
    gem_scraper.append_data_to_csv()

if __name__ == "__main__":
    mainFunction()