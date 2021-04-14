from WebScraper import WebScraper 
import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time
import math

class YellowPages2(WebScraper):
    def __init__(self, keywords):
        super().__init__(keywords)

    def get_urls(self):
        temp_url_list = []
        WEBSITE_PREFIX = "https://www.yellowpagesofafrica.com"

        URL = 'https://www.yellowpagesofafrica.com/country/madagascar'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='col-sm-9 col-lg-10 ct-u-marginBottom20')
        categories = results.find_all('div', class_='row')
        for category in categories:
            companies = category.find_all('a')
            for company in companies:
                title = company.find('h3', class_='activites')
                title = title.text.strip().lower()
                link = company['href']
                temp_url_list.append((title, link))

        # clean list to match keywords
        for (name, website) in temp_url_list:
            if any(word in name for word in self.keywords):
                self.url_list.append(WEBSITE_PREFIX + website)
    
    def parse(self): 
        # url list is by category 
        self.get_urls()

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        DRIVER_PATH = '/Users/cathleen/Downloads/chromedriver'
        browser = webdriver.Chrome(executable_path=DRIVER_PATH, options = options)

        for url in self.url_list: 
            print(url)
            browser.get(url + "start-1/") 

            # get all results page from that category 
            resultNum = browser.find_element_by_xpath("//h2[contains(@class, 'text-uppercase ct-u-marginBottom10')]")
            resultNum = resultNum.text[13:-1]
            numResultPages = math.ceil(int(resultNum) / 10.0)
            search_pages = []
            search_pages.append(url + "start-1/")
            for i in range(1, int(numResultPages)):
                search_pages.append(url + "start-" + str(i) + "1/")

            service = url[57:-1]
            
            for page in search_pages: 
                # parse page 
                browser.get(page) 
                product_titles = browser.find_elements_by_class_name('ct-product--tilte')
                locations = browser.find_elements_by_class_name('ct-product--description')
                websites = browser.find_elements_by_id('a')
                show_info_btn = browser.find_elements_by_class_name('buttonShowCo')
                i = 0
                parse_str_len = 25 
                START_KEYWORD = "See"
                END_KEYWORD = "emails"

                for btn in show_info_btn:
                    coordinates = btn.location_once_scrolled_into_view 
                    browser.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
                    time.sleep(1)
                    btn.click()
                    time.sleep(1)

                contact_info = browser.find_elements_by_xpath("//*[contains(@id, 'coordonnees')]")

                for title in product_titles:
                    business = {} 
                    full_text = locations[i].text
                    full_text = full_text.replace('\n', ' ')
                    start_parse_index = full_text.find(START_KEYWORD)
                    end_parse_index = full_text.find(END_KEYWORD) + 6
                    location = full_text[:start_parse_index].rstrip()
                    website = full_text[end_parse_index:].strip('\n')
                    business['name'] = title.text 
                    business['service'] = service
                    business['search_term'] = service
                    business['location'] = location
                    business['phone'] = website
                    business['website'] = website
                    business['email'] = website 
                    
                    i+=1
                    self.business_list.append(business)
        print(len(self.business_list))
        browser.quit()
        