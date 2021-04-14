import csv 

class WebScraper:
    def __init__(self):
        self.keywords = ['transportation', 'construction', 'furniture', 'office', 
                        'school supplies', 'material', 'concrete', 'mud brick', 
                        'thatched roofing', 'truck', 'freight', 'train', 'utility', 
                        'electricity', 'sewage','building materials', 'hardware', 
                        'wood', 'roofs','solar panel', 'water tank','crane','plumbing',
                        'artisan','hotel','taxi']
        self.csv_columns = ['name', 'search_term', 'service', 'location', 'phone', 'email', 'website', 'latitude', 'longitude', 'rating']
        self.business_list = []
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
