from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


class GoogleMapWebScraper:

    def __init__(self, search_terms=[], coordinates=(-19.8292149, 45.5268368), zoom=6.91, phone_extension='+261'):
        self.search_terms = search_terms
        # self.fields_to_collect = fields_to_collect
        self.coordinates = coordinates
        self.zoom = zoom
        self.url_list = self.get_urls()
        self.browser = webdriver.Chrome(
            'C:/Users/jazka/Documents/chromedriver.exe')
        self.business_lst = []
        self.phone_extension = phone_extension

    def get_urls(self):
        """
        Convert the terms and coordinates into urls
        """
        urls = []
        for term in terms:

            # Convert spaces to + signs as used in Google Maps
            term_lst = term.split(' ')
            term = ''
            for term_part in term_lst:
                term += term_part + '+'

            urls.append('https://www.google.com/maps/search/' +
                        term + '/@' + str(self.coordinates[0]) + ',' + str(self.coordinates[1]) + ',' + str(self.zoom) + 'z')

        return urls

    def get_sources(self):
        """
        Scrape sources from the given google maps url of a search at a given location. For each company, 
        get the name, service provided, location, and phone number if available.
        """
        business_lst = []
        i = 0
        for url in self.url_list:
            print(url)
            self.browser.get(url)

            time.sleep(7)

            # Zoom in so that "Search this area" button will show up
            self.browser.find_element_by_id('widget-zoom-in').click()

            time.sleep(3)

            # Must hit  "Search this area", otherwise Google defaults to local locations
            self.browser.find_element_by_class_name(
                'widget-search-this-area-inner').click()

            time.sleep(5)

            htmlstring = self.browser.page_source
            soup = BeautifulSoup(htmlstring, "html.parser")
            results = soup.find_all(class_='section-result-content')

            for result in results:
                name = result.find(class_='section-result-title').text
                service = result.find(class_='section-result-details').text

                # Default to the seach term if no service provided was found
                if service == '':
                    service = search_terms[i]

                location = result.find(class_='section-result-location').text
                phone = result.find(
                    class_='section-result-info section-result-phone-number').text

                # Get rid of phone numbers with the wrong extension. These may come from your ip address location!
                if phone.strip()[0:len(self.phone_extension)] != self.phone_extension:
                    phone = ''

                business_lst.append(
                    {'name': name, 'service': service, 'location': location, 'phone': phone})
            self.business_lst = business_lst
            i += 1
        return business_lst

    def write_data_to_csv(self, filename):
        """
        Writes the data collected in get_sources() to a csv file
        """
        csv_columns = ['name', 'service', 'location', 'phone']
        try:
            with open(filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self.business_lst:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


terms = ['Transportation', 'Construction', 'Furniture', 'Office', 'school supplies', 'Material', 'Concrete',
         'Mud brick', 'Thatched roofing', 'Truck', 'Freight', 'train', 'Utility', 'Electricity', 'Sewage']
scraper = GoogleMapWebScraper(terms)
scraper.get_sources()
scraper.write_data_to_csv('google_maps_data_Transport.csv')
