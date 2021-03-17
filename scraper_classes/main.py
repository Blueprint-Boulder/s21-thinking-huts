from YellowPages1 import YellowPages1 

def mainFunction():
    yellow_pages1 = YellowPages1()
    yellow_pages1.parse() 
    yellow_pages1.write_data_to_csv()

if __name__ == "__main__":
    mainFunction()