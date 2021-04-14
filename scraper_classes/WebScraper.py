import csv 

class WebScraper:
    def __init__(self):
        self.keywords = keywords
        self.csv_columns = ['name', 'search_term', 'service', 'location', 'phone', 'email', 'website', 'latitude', 'longitude', 'rating']
        self.business_list = []
        self.filename = "madagascar-business.csv"
        self.url_list = []
    
    def set_keywords(self, keywords):
        self.keywords = keywords
    
    def write_data_to_csv(self):
        try:
            with open(self.filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                writer.writeheader()
                for data in self.business_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    def append_data_to_csv(self):
        try:
            with open(self.filename, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                for data in self.business_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
