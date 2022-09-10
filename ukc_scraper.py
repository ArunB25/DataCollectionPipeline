from cgitb import text
from itertools import count
from lib2to3.pgen2 import driver
from multiprocessing.sharedctypes import Value
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tabulate import tabulate

class scraper:

    def __init__(self):
        """
        initialises the starting variables
        """
        self.crags = {'Name':[], 'URL':[], 'RockType':[]}
        self.climb = {'Name': [], 'Crag': [], 'Grade': [], 'Stars': [], 'Type': [], 'Guidebook': [], 'Description': []}
    
    def load_and_accept_cookies(self) -> webdriver.Chrome:
        '''
        Open UKC and accept the cookies. Using the chrome web driver
        '''
        self.driver = webdriver.Chrome() 
        URL = "https://www.ukclimbing.com/logbook/books/"
        self.driver.get(URL)
        time.sleep(1) 
        accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@class = "btn btn-primary"]')
        accept_cookies_button.click()
        time.sleep(1)

    def get_guidebooks(self,input_country):
        """
        scrapes the current page for all the guidebooks of the specified country 
        """    
        country_list = self.driver.find_elements(By.XPATH, '//div[@class = "card mb-2"]')

        for country in country_list: #search through all countrys cards
            a_tag = country.find_element(By.TAG_NAME, 'a')
            a_text = a_tag.text
            if input_country.lower() in a_text.lower():  #if country matches inputed country break
                break
        
        print(country.find_element(By.TAG_NAME, 'a').text)
        guidebook_card = country.find_element(By.XPATH, './/div[@class = "card-body"]')
        all_guidebooks = guidebook_card.find_elements(By.TAG_NAME, 'li')    #get list of all guide books in specified country
        OutofPrint_list = guidebook_card.find_elements(By.XPATH, './/li[@title = "Out of print"]')  #get list of all out of print guide books in specified country
        guidebooks_inprint = [x for x in all_guidebooks if x not in OutofPrint_list] #remove guide books that are no longer being printed

        self.guidebook_links = []
        for guide in guidebooks_inprint: #gets links for all guidebooks
            a_tag = guide.find_element(by=By.TAG_NAME, value='a')
            self.guidebook_links.append(a_tag.get_attribute('href'))

        print(f"{len(self.guidebook_links)} guidebooks in print in {input_country}")

    def get_crags(self,guidebook_URL):
        """
        scrapes the guidebook page for all the crags and stores there name,URL and rocktype
        """   
        self.driver.get(guidebook_URL)
        print(guidebook_URL)
        try:
            crag_tables = self.driver.find_elements(By.CLASS_NAME,"col-sm-6") 
            rows = []
            headers = []
            for table in crag_tables:
                rows = rows + table.find_elements(By.TAG_NAME, "tr")
                headers = headers + table.find_elements(By.CLASS_NAME, 'hdr1')

            crag_rows = [x for x in rows if x not in headers] #Remove headers from rows

            for row in crag_rows:
                    a_tag = row.find_element(By.TAG_NAME, 'a')
                    self.crags['URL'].append(a_tag.get_attribute('href'))
                    self.crags['Name'].append(a_tag.text)
                    self.crags['RockType'].append(row.find_element(By.XPATH, './td[3]').text)
        except:
            print("no crags for this guidebook")
        time.sleep(1)

    def get_climbs(self,crag_link):
        self.driver.get(crag_link)
        table = self.driver.find_element(By.ID, 'climb_table')
        table_body = table.find_element(By.TAG_NAME, 'tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')
        buttress_list = table_body.find_elements(By.XPATH, './/tr[@class ="dtrg-group buttress_header dtrg-start dtrg-level-0"]')
        
        for row in rows:
            if row in buttress_list:
                buttress = row.find_element(By.TAG_NAME, 'h5').text
                print(buttress)
            elif row not in buttress_list:
                a_tag = row.find_element(By.XPATH, './/*[@class = "small not-small-md main_link"]')
                print(a_tag.text)
            else:
                print("what is this row????")


        





if __name__ == "__main__":
    
    eng_climbs = scraper()
    eng_climbs.load_and_accept_cookies()
    eng_climbs.get_guidebooks("England")
    eng_climbs.get_crags(eng_climbs.guidebook_links[0])
    print(eng_climbs.crags.get('URL',1)[0])
    eng_climbs.get_climbs(eng_climbs.crags.get('URL',1)[0])