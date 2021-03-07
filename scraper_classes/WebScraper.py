import csv 

class WebScraper:
    def __init__(self):
        self.keywords = ['Transportation', 'Construction', 'Furniture', 'Office', 
                        'school supplies', 'Material', 'Concrete', 'Mud brick', 
                        'Thatched roofing', 'Truck', 'Freight', 'train', 'Utility', 
                        'Electricity', 'Sewage']
        self.csv_columns = ['name', 'search_term', 'service', 'location', 'phone', 'email', 'website', 'Latitude', 'Longitude', 'Favorite']
        self.business_list = {}
        self.filename = "madagascar-business.csv"
    
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
