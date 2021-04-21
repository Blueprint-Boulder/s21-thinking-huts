from bs4 import BeautifulSoup
import csv

from WebScraper import WebScraper 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class GoogleMapScraper(WebScraper):

    def __init__(self, wait_time=3, coordinates=(-19.8292149, 45.5268368), zoom=6.91):
        
        super().__init__()

        self.wait_time = wait_time
        self.coordinates = coordinates
        self.zoom = zoom
        self.url_list = self.get_urls()
        self.browser = webdriver.Chrome(
            'C:/Users/jazka/Documents/chromedriver.exe')
        self.business_url_tuples = []
        

    def get_urls(self):
        """
        Convert the terms and coordinates into urls
        """
        urls = []
        for term in self.keywords:

            # Convert spaces to + signs as used in Google Maps
            term_lst = term.split(' ')
            term = ''
            for term_part in term_lst:
                term += term_part + '+'

            urls.append('https://www.google.com/maps/search/' +
                        term + '/@' + str(self.coordinates[0]) + ',' + str(self.coordinates[1]) + ',' + str(self.zoom) + 'z')

        return urls

    def get_business_urls(self):
        i = 0
        for url in self.url_list:
            self.browser.get(url)

            time.sleep(self.wait_time)
            try:
                # Zoom in so that "Search this area" button will show up
                self.browser.find_element_by_id('widget-zoom-in').click()
            except:
                print("Zoom didn't load, try increasing the wait time")

            time.sleep(self.wait_time)

            try:
                # Must hit  "Search this area", otherwise Google defaults to local locations
                self.browser.find_element_by_class_name(
                    'widget-search-this-area-inner').click()
            except:
                print("Search This Area button didn't load, try increasing the wait time")

            while True:
                time.sleep(self.wait_time)
                elements = self.browser.find_elements_by_xpath('//a')
                # self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",element)
                for element in elements:
                    try:
                        url = element.get_attribute('href')
                        if 'https://www.google.com/maps/place' in url:
                            self.business_url_tuples.append((url,self.keywords[i]))
                    except:
                        pass
                try:
                    nxt_btn = self.browser.find_element_by_id('n7lv7yjyC35__section-pagination-button-next')
                except:
                    break
                if nxt_btn.get_attribute("disabled") == 'true':
                    break
                try:
                    nxt_btn.click()
                except:
                    break
            i += 1

    def parse(self):
        """
        Scrape sources from the given google maps url of a search at a given location. For each company, 
        get the name, service provided, location, and phone number if available.
        """
        for url_tuple in self.business_url_tuples:
            self.browser.get(url_tuple[0])
            time.sleep(self.wait_time)
            
            try:
                rating = scraper.browser.find_element_by_class_name("section-star-display").text
            except:
                rating = ''
            try:
                service = scraper.browser.find_element_by_class_name('section-rating').text.split('\n')[-1]
            except:
                service = ''
            try:
                name = scraper.browser.find_element_by_class_name("section-hero-header-title-title").text
            except:
                name = ''
            try:
                address = scraper.browser.find_element_by_css_selector("[data-item-id='address']").text.replace(',', '')
            except:
                address = ''
            try:
                phone_number = scraper.browser.find_element_by_css_selector("[data-tooltip='Copy phone number']").text
            except:
                phone_number = ''
            try:
                website = scraper.browser.find_element_by_css_selector("[data-item-id='authority']").text
            except:
                website = ''
            self.business_list.append(
                     {'name': name, 'search_term': url_tuple[1], 'service': service, 'location': address, 'phone': phone_number,'rating':rating,'website':website})

            
if __name__ == "__main__":
    keywords = ['transportation', 'construction', 'furniture', 'office', 
                        'school supplies', 'material', 'concrete', 'mud brick', 
                        'thatched roofing', 'truck', 'freight', 'train', 'utility', 
                        'electricity', 'sewage','building materials', 'hardware', 
                        'wood', 'roofs','solar panel', 'water tank','crane','plumbing',
                        'artisan','hotel','taxi']
    scraper = GoogleMapScraper(keywords,wait_time=5)
    scraper.get_business_urls()
    scraper.parse()
    scraper.write_data_to_csv()
