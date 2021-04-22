from WebScraper import WebScraper 
import requests
from bs4 import BeautifulSoup
import csv

class YellowPages1(WebScraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def get_urls(self):
        '''
          Compile a list of all urls to search 
        '''
        url_list = []
        for i in range(1, 22):
            url_list.append('http://www.business-yellowpages.com/madagascar/page-' + str(i))
        return url_list
    
    def parse(self): 
        '''
          Parse and get business dictionaries from all URLs in url_list
        '''
        url_list = self.get_urls()
        
        for url in url_list:
            page = requests.get(url) 
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='List-of-companies')
            jobs = results.find_all('dl')

            for job in jobs:
                business = {} 

                link = job.find('a')['href']
                name = job.find('a').string
                business["name"] = name
                business["website"] = link 

                other_fields = job.find_all('dd')
                for field in other_fields:
                    if len(field.contents) == 1:
                        continue
                    field_label = field.contents[0].find_all(text=True, recursive=False)[0]
                    elem = field.contents[1]

                    if ("Tel" in field_label):
                        business["phone"] = elem  
                    elif ("Address" in field_label):  
                        formatted_loc = elem.replace("\n", " ")  
                        formatted_loc = formatted_loc.replace("\r", "")  
                        business["location"] = formatted_loc
                    elif ("Main Products" in field_label):
                        business["service"] = elem
                    else:
                        continue 

                self.business_list.append(business)    
        self.cleanup_business_list()

    def cleanup_business_list(self):
          '''
          Look for keywords in main products to see if business is relevant 
          '''
          i = 0
          temp_business_list = self.business_list.copy()
          for entry in temp_business_list:
              services = entry['service']
              services = services.lower()
              if not any(word in services for word in self.keywords):
                  self.business_list.remove(entry)


