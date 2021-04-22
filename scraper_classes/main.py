from YellowPages1 import YellowPages1 
from YellowPages2 import YellowPages2

def mainFunction():
    keywords = ['transportation', 'construction', 'furniture', 'office', 
                        'school supplies', 'material', 'concrete', 'mud brick', 
                        'thatched roofing', 'truck', 'freight', 'train', 'utility', 
                        'electricity', 'sewage','building materials', 'hardware', 
                        'wood', 'roofs','solar panel', 'water tank','crane','plumbing',
                        'artisan','hotel','taxi']
    yellow_pages1 = YellowPages1(keywords)
    yellow_pages1.parse() 
    yellow_pages1.write_data_to_csv()
    yellow_pages2 = YellowPages2(keywords)
    yellow_pages2.parse()
    yellow_pages2.write_data_to_csv()

if __name__ == "__main__":
    mainFunction()