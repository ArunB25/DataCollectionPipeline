from itertools import count
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class scraper:

    def __init__(self):
        """
        initialises the starting variables
        """

        self.climb = {'Name': [], 'Crag': [], 'Grade': [], 'Stars': [], 'Type': [], 'Guidebook': [], 'Description': []}
    
    def load_and_accept_cookies(self) -> webdriver.Chrome:
        '''
        Open UKC and accept the cookies. Using the chrome web driver
        '''
        self.driver = webdriver.Chrome() 
        URL = "https://www.ukclimbing.com/logbook/books/"
        self.driver.get(URL)
        time.sleep(3) 
        accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@class = "btn btn-primary"]')
        accept_cookies_button.click()
        time.sleep(1)

    def get_guidebooks(self,input_country):
        """
        scrapes the current page for all the guidebooks of the specified country 
        """    
        country_list = self.driver.find_elements(By.XPATH, f'//div[@class = "card mb-2"]')

        for country in country_list:
            a_tag = country.find_element(by=By.TAG_NAME, value='a')
            a_text = a_tag.text
            if input_country.lower() in a_text.lower():
                print(a_text)
                break
        
        guidebook_list = country.find_elements(By.XPATH, f'//div[@class = "card mb-2"]')






    def get_property_details(self,property_link):
        """
        Takes the property URL and scrapes to find the Price, address, number of bedrooms and descripton and adds them to the dictionary of properties
        """
        self.driver.get(property_link)
        try:
            price = self.driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
            self.dict_properties['Price'].append(price)
        except:
            self.dict_properties['Price'].append("NA")
        try:
            address = self.driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
            self.dict_properties['Address'].append(address)
        except:
            self.dict_properties['Address'].append("NA")
        try:
            rooms = self.driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]')
            bedrooms = rooms.find_element(by=By.XPATH, value='//div[@class="c-cbuYEU c-cbuYEU-egQFzo-isAnAttribute-true c-cbuYEU-iPJLV-css"]').text
            self.dict_properties['Bedrooms'].append(bedrooms)
        except:
            self.dict_properties['Bedrooms'].append("NA")
        try:
            div_tag = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
            span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
            description = span_tag.text
            self.dict_properties['Description'].append(description)
        except:
            self.dict_properties['Description'].append("NA")
        
        time.sleep(1)

if __name__ == "__main__":
    
    eng_climbs = scraper()
    eng_climbs.load_and_accept_cookies()
    eng_climbs.get_guidebooks("England")