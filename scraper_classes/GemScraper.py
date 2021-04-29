import time
from WebScraper import WebScraper
from selenium import webdriver
from bs4 import BeautifulSoup

class GemScraper(WebScraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def getUrls(self):
        return self.url_list

    def getBusinessList(self):
        return self.business_list

    def parse(self): 

        browser = webdriver.Chrome('') # Take in chromedriver directory
        browser.get('http://www.gem-madagascar.com/membres')

        html_string = browser.page_source
        soup = BeautifulSoup(html_string, "html.parser")

        businesses = soup.find_all('a', href = True)

        for business in businesses:
            member = business['href'].startswith('/membre/')
            if (member):
                url_id = business['href'][8:]
                self.url_list.append('http://www.gem-madagascar.com/membre/{}'.format(url_id))
        
        time.sleep(1)
        browser.quit()

    def parseBusinessPages(self):

        for business_webpage in self.url_list:

            business = dict()

            browser = webdriver.Chrome('') # Take in chromedriver directory
            browser.get(business_webpage)

            html_string = browser.page_source
            soup = BeautifulSoup(html_string, "html.parser")

            business_info = soup.find_all('tbody', class_ = 'informations-entreprises-membres')[1]

            business_name = soup.find_all('cufontext')[4:-8]

            name = ""
            for element in business_name:
                name += element.get_text() + " "
            
            # Name
            business['name'] = name
            # Address 
            business['location'] = business_info.find_all('td')[1].get_text().strip()
            # Phone Number
            business['phone'] = business_info.find_all('td')[3].get_text().strip()
            # Fax 
            # business['Fax'] = business_info.find_all('td')[5].get_text().strip()
            # Email 
            business['email'] = business_info.find_all('td')[7].get_text().strip()
            # Website
            business['website'] = business_info.find_all('td')[9].get_text().strip()

            self.business_list.append(business)

            time.sleep(1) 
            browser.quit()

gem = GemScraper('')
# Grabs all business URLs
gem.parse()
# Parse each individual business page
gem.parseBusinessPages()
# Return list of businesses and their info
gem.getBusinessList
