
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from WebScraper import WebScraper 


class LinkedInScraper(WebScraper):

	def __init__(self, keywords,chromedriver_path = './chromedriver-mac.exe', chrome_extension_path = './salesql-browser-extension-v4.0.1'):
		super().__init__(keywords)
		self.option = webdriver.ChromeOptions()
		self.option.add_argument('--load-extension=' + chrome_extension_path)
		self.driver = webdriver.Chrome(chromedriver_path,options = self.option)


	def addExtension(self):
		#adds chrome extension to browser
		self.driver.get('chrome-extension://mloghaifglppagfgdjjjabofpbebdnbl/popup/popup.html')
		self.driver.switch_to.window(self.driver.window_handles[0])
		

		#login to chrome extension
		username = '100457400@alumnos.uc3m.es'
		password = 'email1234#'
		email_ext = self.driver.find_element_by_xpath('/html/body/div/div/div/div[4]/div/input') 
		email_ext.send_keys(username)
		password_ext = self.driver.find_element_by_xpath('/html/body/div/div/div/div[5]/div/input')
		time.sleep(5)
		password_ext.send_keys(password)
		self.driver.find_element_by_xpath('/html/body/div/div/div/button').click()



	def loginToLinkedIn(self):
		#logs in to linkedin 
		LinkedinUN = 'hastingsj890@gmail.com'
		password = 'email1234#'
		self.driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
		time.sleep(5)
		LinkedIN_us = self.driver.find_element_by_id('username')
		LinkedIN_pw = self.driver.find_element_by_id('password')
		LinkedIN_pw.send_keys(password)
		LinkedIN_us.send_keys(LinkedinUN)
		self.driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()

		if "https://www.linkedin.com/checkpoint/challenge/" in self.driver.current_url:  #checks if linkedin sent a security checkpoint
			print("login into hastingsj890@gmail.com with password email1234# and retrieve the verification code")
			time.sleep(60)
		




	def checkingList(self,item,results):
		#checks see if the item already exists in the list 
		if len(results) > 0:
			if item in results:
				return True
		return False		


	def parseProfile(self,url):
		#scrapes the name of company and locations off the linkedin profile page
		self.driver.get(url)	
		self.driver.maximize_window()
		time.sleep(5)
		company_page = self.driver.page_source  
		linkedin_soup = BeautifulSoup(company_page.encode("utf-8"), "html.parser")
		linkedin_soup.prettify()
		information = linkedin_soup.find("section",{"class": "artdeco-card ember-view pv-top-card"})
		if information is None: # checks to see if html tag section was found if not exit the function 
			return []
		else:
			title = information.find("h1").text.strip()
			location = linkedin_soup.find("span",{"class":"text-body-small inline t-black--light break-words"}).text.strip()
		
		return [title,location]



	def googleUrlSearch(self,URL,keyword):
		#scrapes revelant linkedin profiles based on keyword passed and returns the information about the company or person in a list of dictionaries 
		self.driver.get(URL)
		html = self.driver.page_source
		search_result = BeautifulSoup(html.encode("utf-8"), "html.parser")
		search_result.prettify()
		containers = search_result.findAll("div",{"class":"g"})
		results = []
		info = []

		for container in containers: #loops through all google search results
			anchors = container.find_all('a')
			if anchors:
				link = anchors[0]['href']
				if "linkedin.com/in" in link: 
					info = self.parseProfile(link)
					time.sleep(1)
					if len(info) == 0:
						continue

					
					if 'Madagascar' in info[1] or 'madagascar' in info[1]:         #checks to see if companies or the person's location is in madagascar			
						profile_information = {
							'name' : info[0],
							'search_term': keyword, 
							'service': keyword, 
							'location': info[1], 
							'phone': '-',
							'email': '-',
							'rating':'-',
							'website': link
						}
						if self.checkingList(profile_information,results) == False:  #checks to see that the profile hasn't already been scrapped and added to list of revelant profiles
							results.append(profile_information)
		
				
			time.sleep(1)		

		return results

	
	def creatingBusinessList(self):

		#searchs the first 3 pages of google and saves all the information from linkedin profile into the business_list list


		page = 0
		results = []
		for keyword in self.keywords:
			query = "madagascar AND " +  keyword +" linkedin"
			#first page of google
			URL = 'https://www.google.com/search?q={}&ei=5P6aYNaNH4_btQas_q_ABw&start={}&sa=N&ved=2ahUKEwjWj-ne0MLwAhWPbc0KHSz_C3g4ChDx0wN6BAgBEDM&biw=1440&bih=789'.format(query,0)
			self.driver.get(URL)
			results.extend(self.googleUrlSearch(URL, keyword))  #populates the list results  with dictionaries containing all the necessary information from each linkedin profile
			time.sleep(5)
			#second page of google
			URL = 'https://www.google.com/search?q={}&ei=ZPyaYJ3DM9nVtAa9w4SwBQ&start={}&sa=N&ved=2ahUKEwidheetzsLwAhXZKs0KHb0hAVYQ8NMDegQIARBI&biw=1440&bih=789'.format(query,10)
			self.driver.get(URL)
			results.extend(self.googleUrlSearch(URL, keyword))
			time.sleep(5)	
			# third page of google
			URL = 'https://www.google.com/search?q={}&ei=XgGbYO-CCJvbtAb977nYDw&start={}&sa=N&ved=2ahUKEwjvqfqM08LwAhWbLc0KHf13Dvs4ChDy0wN6BAgBEDk&biw=1440&bih=789'.format(query,20)
			self.driver.get(URL)
			results.extend(self.googleUrlSearch(URL, keyword))
			time.sleep(5)

			self.business_list.extend(results)	
			results = []




if __name__ == "__main__":
	# start = time.time()
	keywords = ['transportation', 'construction','furniture', 'office', 
                       'school supplies', 'material', 'concrete', 'mud brick', 
                        'thatched roofing', 'truck', 'freight', 'train', 'utility', 
                        'electricity', 'sewage','building materials', 'hardware', 
                        'wood', 'roofs','solar panel', 'water tank','crane','plumbing',
                        'artisan','hotel','taxi']
	scraper = LinkedInScraper(keywords)
	scraper.addExtension()
	scraper.loginToLinkedIn()
	time.sleep(5)
	scraper.creatingBusinessList()
	scraper.write_data_to_csv()
	# end = time.time()
	# print(f"Runtime of the program is {end - start}")


























