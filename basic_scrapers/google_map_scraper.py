from selenium import webdriver
from bs4 import BeautifulSoup
import time

browser = webdriver.Chrome('C:/Users/jazka/Documents/chromedriver.exe')


def get_sources(url, term):
    """
    Scrape sources from the given google maps url of a search at a given location. For each company, 
    get the name, service provided, location, and phone number if available.
    """
    # url = 'https://www.google.com/maps/search/carpentry/@-19.8292149,45.5268368,6.91z'

    browser.get(url)

    time.sleep(5)

    # Zoom in so that "Search this area" button will show up
    browser.find_element_by_id('widget-zoom-in').click()

    time.sleep(2)

    # Must hit  "Search this area", otherwise Google defaults to local locations
    browser.find_element_by_class_name('widget-search-this-area-inner').click()

    time.sleep(2)

    # For future clicking on each company and getting more info
    # results = browser.find_elements_by_class_name('section-result-content')
    # for result in results:
    #     result.click()
    #     time.sleep(2)
    #     htmlstring = browser.page_source
    #     company_soup = BeautifulSoup(htmlstring, "html.parser")
    #     print(company_soup.find(class_='section-layout').text)
    #     browser.find_element_by_class_name(
    #         'section-back-to-list-button').click()
    #     time.sleep(2)

    htmlstring = browser.page_source

    soup = BeautifulSoup(htmlstring, "html.parser")

    results = soup.find_all(class_='section-result-content')

    business_dict = {}

    for result in results:
        name = result.find(class_='section-result-title').text
        service = result.find(class_='section-result-details').text

        # Default to the seach term if no service provided was found
        if service == '':
            service = term

        location = result.find(class_='section-result-location').text
        phone = result.find(
            class_='section-result-info section-result-phone-number').text
        business_dict[name] = [service, location, phone]
        # print(name)
        # print(service)
        # print(location)
        # print(phone)
        # print()
    return business_dict


terms = ['Transportation', 'Construction', 'Furniture', 'Office', 'school supplies', 'Material', 'Concrete',
         'Mud brick', 'Thatched roofing', 'Truck', 'Freight', 'train', 'Utility', 'Electricity', 'Sewage']
# terms = ['freight']
for term in terms:
    # print('\n\n')
    # print(term)
    # print()
    business_dict = get_sources('https://www.google.com/maps/search/' +
                                term + '/@-19.8292149,45.5268368,6.91z', term)

    print(business_dict)
