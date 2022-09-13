from ast import main
from cgitb import text
from itertools import count
from lib2to3.pgen2 import driver
from multiprocessing.sharedctypes import Value
from turtle import tilt, title
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from tabulate import tabulate

class scraper:
    
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
        scrapes the guidebook page for all the crags and returns a dictionary, where each item is the crags name and init is a list with the URL, Rocktype and empty route dictionary
        """   
        self.driver.get(guidebook_URL)
        try:
            crag_tables = self.driver.find_elements(By.CLASS_NAME,"col-sm-6") 
            rows = []
            headers = []
            for table in crag_tables:
                rows = rows + table.find_elements(By.TAG_NAME, "tr")
                headers = headers + table.find_elements(By.CLASS_NAME, 'hdr1')

            crag_rows = [x for x in rows if x not in headers] #Remove headers from rows
            crags = {}
            crag_routes = {}
            for row in crag_rows:
                    a_tag = row.find_element(By.TAG_NAME, 'a')
                    crag_url = a_tag.get_attribute('href')
                    crag_name = a_tag.text
                    crag_rocktype = row.find_element(By.XPATH, './td[3]').text
                    crags[crag_name] = [crag_url,crag_rocktype,crag_routes]
        except:
            print("no crags for this guidebook")
        time.sleep(1)
        return(crags)

    def get_routes(self,crag):
        """
        scrapes the crag page for all the route and returns a dictionary of buttresses which contain a dictionary of every route at the buttress
        """
        crag_URL = crag[0]
        self.driver.get(crag_URL)
        table = self.driver.find_element(By.ID, 'climb_table')
        table_body = table.find_element(By.TAG_NAME, 'tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')
        buttress_list = table_body.find_elements(By.XPATH, './/tr[@class ="dtrg-group buttress_header dtrg-start dtrg-level-0"]')
        buttress_dict = {}
        route_details = []
        for row in rows:
            if row in buttress_list:
                if len(route_details) != 0:
                    buttress_dict[buttress] = routes_dict
                buttress = row.find_element(By.TAG_NAME, 'h5').text
                routes_dict = {}
            elif row not in buttress_list:
                route_details = []
                a_tag = row.find_element(By.XPATH, './/*[@class = "small not-small-md main_link "]')
                route_name = a_tag.text
                route_details.append(a_tag.get_attribute('href'))
                climbing_type= row.find_element(By.XPATH, './/td[@class = " datatable_column_type"]')
                route_details.append(climbing_type.find_element(By.TAG_NAME, 'i').get_attribute('title'))
                grade = row.find_element(By.XPATH, './/td[@class = " datatable_column_grade small not-small-md"]')
                route_details.append(grade.find_element(By.TAG_NAME, "span").text)
                stars= row.find_element(By.XPATH, './/td[@class = " datatable_column_star"]')
                try:    
                    route_details.append(stars.find_element(By.TAG_NAME, 'i').get_attribute('title'))
                    
                except:
                    route_details.append("None")
                routes_dict[route_name] = route_details
            else:
                print("what is this row????")
        return(buttress_dict)

    def get_cragPics(self,crag):
        crag_URL = crag[0]
        self.driver.get(crag_URL)
        pics_tab = self.driver.find_element(By.ID, 'show_photos').get_attribute('href')
        self.driver.get(pics_tab)
        self.driver.refresh()
        time.sleep(1)
        photos_list = self.driver.find_elements(By.XPATH, '//a[@class = "photoswipe"]')
        images = {}
        for photo in photos_list:
            photo_src = photo.get_attribute('data-image')
            img_thumbnail = photo.find_element(By.CLASS_NAME, 'img-fluid')
            title = (img_thumbnail.get_attribute('alt')).split('<',1)[0]
            images[title] = photo_src
        
        print(images)



if __name__ == "__main__":
    
    eng_climbs = scraper()
    eng_climbs.load_and_accept_cookies()
    eng_climbs.get_guidebooks("England")
    eng_climbs.crags = eng_climbs.get_crags(eng_climbs.guidebook_links[0])
    first_crag = list(eng_climbs.crags.keys())[0]

    eng_climbs.get_cragPics(eng_climbs.crags[first_crag])

    #eng_climbs.crags[first_crag][2] = eng_climbs.get_routes(eng_climbs.crags[first_crag])
    #print(eng_climbs.crags[first_crag])

    