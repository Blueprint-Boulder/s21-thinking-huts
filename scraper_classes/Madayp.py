from WebScraper import WebScraper 
import requests
from bs4 import BeautifulSoup as bs
import csv

class Madayp(WebScraper):
    def __init__(self,api_key):
        super().__init__('')
        #relevant business categories
        self.api_key = api_key
        self.search_terms = ['Construction','Pumps_Manufacturers','Building_materials','Construction_equipment','Construction_services','Vehicle_services','Transport','Furniture','Furniture_manufacturers','Paper_Products']
        #mapping business category to search keyword for our website display
        self.search_term2key_word = {'Construction':'Construction','Building_materials':'Material','Pumps_Manufacturers':'Water','Construction_equipment':'Construction','Construction_services':'Construction','Vehicle_services':'Truck','Transport':'Truck','Furniture':'school supplies','Furniture_manufacturers':'school supplies','Paper_Products':'school supplies'}

    def write_data_to_csv(self):
        try:
            #uses utf-8 encoding
            with open(self.filename, 'w',encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                writer.writeheader()
                for data in self.business_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


    def get_urls(self,term):
        url_list = []
        base_url = "http://www.madayp.com/category/"
        #Try to find number of pages the business category has
        payload = {'api_key': self.api_key, 'url': base_url+term}
        page_num = 12
        try:
            page = requests.get("http://api.scraperapi.com", params=payload, timeout=60)
            soup = bs(page.content, 'html.parser')
        except:
            return url_list
        try:
            page_container = soup.find(class_="pages_container_top")
            text = page_container.text
            text_split = [int(s) for s in text.split() if s.isdigit()]
            page_num = int(text_split[0]/30)+1
        #If we can't find it, we default to 12 pages which is the max for our categories
        except:
            page_num = 12
        for i in range(1,page_num):
            url_list.append(base_url+term+"/"+str(i))
        return url_list

    def return_business_list(self):
        return self.business_list

    def parse(self):
        #Go through each categories
        for term in self.search_terms:
            #Get all the urls to individual business pages for each category
            url_list = self.get_urls(term)
            all_urls=[]
            all_urls_only=[]
            for url in url_list:
                payload = {'api_key': self.api_key, 'url': url}
                try:
                    page = requests.get("http://api.scraperapi.com", params=payload, timeout=60)
                except:
                    continue
                #parse
                soup1=bs(page.content, 'html.parser')
                results=soup1.find_all(class_="company g_0")
                for company in results:
                    address = company.find(class_="address")
                    a = address.find("a")
                    try:
                        city=a.text
                    except:
                        city = ''
                    for site in company:
                        a = site.find('a', href=True)
                        try:
                            url=a['href']
                            if url not in all_urls_only:
                                all_urls.append([url,city])
                                all_urls_only.append(url)

                        except:
                            continue

            for url in all_urls:
                if 'company' not in url[0]:
                    continue
                url[0]="http://www.madayp.com"+url[0]
                print(url[0])
                payload = {'api_key': self.api_key, 'url': url[0]}
                try:
                    page = requests.get("http://api.scraperapi.com",params=payload, timeout=60)
                except:
                    continue
                soup2=bs(page.content, 'html.parser')
                business = {}
                fields = [0,0,0,0]
                fields[0]=soup2.find(id = "company_name")
                fields[2]=soup2.find(class_ = "text phone")
                fields[3]=soup2.find(class_ = "text weblinks")
                fields[1]=soup2.find(class_ = "city523")
                for i in range(0,3):
                    try:
                        fields[i] = fields[i].contents[0]
                    except:
                        fields[i]=''

                try:
                    fields[3] = fields[3].contents[0].contents[0]
                except:
                    fields[3]=''

                business["name"] = fields[0]
                business["search_term"]= self.search_term2key_word[term]
                business["location"]=url[1]
                business["phone"]=fields[2]
                business["website"]=fields[3]
                if business["name"]!="":
                    self.business_list.append(business)
