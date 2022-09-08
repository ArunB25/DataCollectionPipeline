from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class scraper:

    def load_and_accept_cookies(self) -> webdriver.Chrome:
        '''
        Open Zoopla and accept the cookies
        
        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the Zoopla webpage
        '''
        self.driver = webdriver.Chrome() 
        URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
        self.driver.get(URL)
        time.sleep(3) 
        try:
            self.driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_elementh(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()
            time.sleep(1)
        except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
            self.driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()
            time.sleep(1)

        except:
            pass

        return self.driver 

    def get_page_links(self):
            
        prop_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]') # XPath corresponding to the Container
        prop_list = prop_container.find_elements(by=By.XPATH, value='./div') 
        self.link_list = []

        for house_property in prop_list:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.link_list.append(link)
            
        print(f'There are {len(self.link_list)} properties in this page')
        print(self.link_list)

if __name__ == "__main__":
    
    lndn_houses = scraper()
    lndn_houses.load_and_accept_cookies()
    lndn_houses.get_page_links()