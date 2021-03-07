from YellowPages1 import YellowPages1 

def mainFunction():
    yellow_pages1 = YellowPages1()
    yellow_pages1.parse() 

# ['name', 'search_term', 'service', 'location', 'phone', 'email', 'website', 'Latitude', 'Longitude', 'Favorite']
    testDict = [{'name': 'testName', 'search_term': 'searchTerm'}, {'name': 'here', 'service': 'Manufacturing'}]
    yellow_pages1.business_list = testDict
    yellow_pages1.append_data_to_csv()

if __name__ == "__main__":
    mainFunction()