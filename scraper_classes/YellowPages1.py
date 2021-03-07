from WebScraper import WebScraper 
import requests
from bs4 import BeautifulSoup
import csv

class YellowPages1(WebScraper):
    def __init__(self):
        super().__init__()

    def get_urls(self):
        #TODO: make list of other URLS
        URL = 'http://www.business-yellowpages.com/madagascar/page-4'
        return URL
    
    def parse(self): 
        url_list = self.get_urls()
        page = requests.get(url_list) 
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='List-of-companies')
        jobs = results.find_all('dl')

        #TODO: put stuff in business list dict 
        # ['name', 'search_term', 'service', 'location', 'phone', 'email', 'website', 'Latitude', 'Longitude', 'Favorite']
        for job in jobs:
        #    title_elem = job_elem.find('dl', class_='title')
        #    company_elem = job_elem.find('div', class_='company')
        #    location_elem = job_elem.find('div', class_='location')
            link = job.find('a')['href']
            name = job.find('a').string
            other_fields = job.find_all('dd')
            print(name)
            print(link)
            for field in other_fields:
                if len(field.contents) == 1:
                    continue
                elem = field.contents[1]
                print(elem)
        #    print(job.prettify())
            print()