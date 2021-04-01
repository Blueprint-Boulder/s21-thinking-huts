from YellowPages1 import YellowPages1 

def mainFunction():
    keywords = ['transportation', 'construction', 'furniture', 'office', 
                'school supplies', 'material', 'concrete', 'mud brick', 
                'thatched roofing', 'truck', 'freight', 'train', 'utility', 
                'electricity', 'sewage']
    

    yellow_pages1 = YellowPages1(keywords)
    yellow_pages1.parse() 
    yellow_pages1.write_data_to_csv()
    # yellow_pages2 = YellowPages2()

if __name__ == "__main__":
    mainFunction()