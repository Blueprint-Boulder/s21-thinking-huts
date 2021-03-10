from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

from WebScraper import WebScraper 


class GoogleMapWebScraper(WebScraper):

    def __init__(self, coordinates=(-19.8292149, 45.5268368), zoom=6.91, phone_extension='+261'):
        
        super().__init__()

        self.coordinates = coordinates
        self.zoom = zoom
        self.url_list = self.get_urls()
        self.browser = webdriver.Chrome(
            'C:/Users/jazka/Documents/chromedriver.exe')
        self.business_list = []
        self.phone_extension = phone_extension

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

    def parse(self):
        """
        Scrape sources from the given google maps url of a search at a given location. For each company, 
        get the name, service provided, location, and phone number if available.
        """
        business_list = []
        i = 0
        for url in self.url_list:
            self.browser.get(url)

            time.sleep(3)
            try:
                # Zoom in so that "Search this area" button will show up
                self.browser.find_element_by_id('widget-zoom-in').click()
            except:
                print("Zoom didn't load, try increasing the wait time")

            time.sleep(3)

            try:
                # Must hit  "Search this area", otherwise Google defaults to local locations
                self.browser.find_element_by_class_name(
                    'widget-search-this-area-inner').click()
            except:
                print("Search This Area button didn't load, try increasing the wait time")


            time.sleep(3)

            htmlstring = self.browser.page_source
            soup = BeautifulSoup(htmlstring, "html.parser")
            results = soup.find_all(class_='section-result-content')

            for result in results:
                name = result.find(class_='section-result-title').text
                service = result.find(class_='section-result-details').text
                search_term = self.keywords[i]

                # Default to the seach term if no service provided was found
                if service == '':
                    service = self.keywords[i]

                location = result.find(class_='section-result-location').text
                phone = result.find(
                    class_='section-result-info section-result-phone-number').text.strip()

                # Get rid of phone numbers with the wrong extension. These may come from your ip address location!
                if phone[0:len(self.phone_extension)] != self.phone_extension:
                    phone = ''
                
                if len(phone) > 0:
                    phone = phone[0:-1]

                business_list.append(
                    {'name': name, 'search_term': search_term, 'service': service, 'location': location, 'phone': phone})
            self.business_list = business_list
            i += 1
        return business_list

if __name__ == "__main__":
    scraper = GoogleMapWebScraper()
    scraper.parse()
    scraper.write_data_to_csv()
