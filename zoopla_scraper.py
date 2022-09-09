from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class scraper:

    def __init__(self):
        """
        initialises the properties links and dictionary and page links
        """
        self.property_links = []
        self.page_links = []
        self.dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Description': []}
    
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
        """
        scrapes the current page for all the properties (regular listings) and puts all the links in a page
        """    
        prop_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]') # XPath corresponding to the Container
        prop_list = prop_container.find_elements(by=By.XPATH, value='./div') 
        

        for house_property in prop_list:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.property_links.append(link)
            
        print(f'There are {len(self.property_links)} properties in this page')
        #print(self.link_list)
        time.sleep(1)

    def next_page(self):
        """
        Gets link from the next page button
        """    
        pagination = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="pagination"]') # XPath corresponding to the pagination section
        pagination = pagination.find_element(by=By.XPATH, value='//ul[@class="e7y3oie8 css-1gny8z8-PaginationContainer-Pagination eaoxhri0"]')
        next_page_button = pagination.find_element(by=By.XPATH, value='//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
        a_tag = next_page_button.find_element(by=By.TAG_NAME, value='a')
        link = a_tag.get_attribute('href')
        self.page_links.append(link)
        time.sleep(1)

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
    
    lndn_houses = scraper()
    lndn_houses.load_and_accept_cookies()

    for page in range(1,5):
        
        lndn_houses.get_page_links()
        lndn_houses.next_page()
        lndn_houses.driver.get(lndn_houses.page_links[(page -1)])

    for i in (lndn_houses.property_links):
        
        lndn_houses.get_property_details(i)

    print(f"There are {len(lndn_houses.dict_properties)} properties in the dictionary")