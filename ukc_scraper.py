from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import uploadto_aws
from selenium.webdriver.chrome.options import Options
class scraper:
    
    def load_and_accept_cookies(self,headless) -> webdriver.Chrome:
        '''
        headless = True or False
        Opens on a chrome web drive UKC and accept the cookies.
        '''
        chromeOptions = Options()
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        if headless == True:
            chromeOptions.headless = True
        else:
            chromeOptions.headless = False


        try:
            self.driver = webdriver.Chrome(options=chromeOptions) 
            URL = "https://www.ukclimbing.com/logbook/books/"
            self.driver.get(URL)
            time.sleep(1) 
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@class = "btn btn-primary"]')
            accept_cookies_button.click()
            time.sleep(1)
            return("Cookies Accepted")
        except:
            return("Error Accepting Cookies")

    def get_guidebooks(self,input_country):
        """
        scrapes the current page for all the guidebooks of the specified country and returns a list of there URLs
        """    
        country_element = self.does_guidebook_country_exist(input_country)
        if country_element == "country not found":
            return("country not found")
        elif country_element == "invalid input":
            return("invalid input")
        else:
            print(country_element.find_element(By.TAG_NAME, 'a').text)
            guidebook_card = country_element.find_element(By.XPATH, './/div[@class = "card-body"]')
            all_guidebooks = guidebook_card.find_elements(By.TAG_NAME, 'li')    #get list of all guide books in specified country
            OutofPrint_list = guidebook_card.find_elements(By.XPATH, './/li[@title = "Out of print"]')  #get list of all out of print guide books in specified country
            guidebooks_inprint = [x for x in all_guidebooks if x not in OutofPrint_list] #remove guide books that are no longer being printed
            guidebook_links = []
            for guide in guidebooks_inprint: #gets links for all guidebooks
                a_tag = guide.find_element(by=By.TAG_NAME, value='a')
                guidebook_links.append(a_tag.get_attribute('href'))

            print(f"{len(guidebook_links)} guidebooks in print in {input_country}")
            return(guidebook_links)
            

    def does_guidebook_country_exist(self,input_country):  
        """
        searches for the input country through the list of countries with guidebooks
        """
        if input_country.isalpha():
            country_list = self.driver.find_elements(By.XPATH, '//div[@class = "card mb-2"]')
            for country in country_list: #search through all countrys cards
                a_tag = country.find_element(By.TAG_NAME, 'a')
                a_text = (a_tag.text).split(' ',1)[0]
                if input_country.lower() == a_text.lower():  #if country matches inputed country break
                    print(a_text)
                    return(country)              
            return("country not found")
        else:
            return("invalid input")

    def get_crags(self,guidebook_URL):
        """
        scrapes the guidebook page for all the crags and returns a dictionary, where each item is the crags name with the URL, Rocktype and empty route & image dictionary
        """   
        self.driver.get(guidebook_URL)
        time.sleep(1)
        mainbody = self.driver.find_element(By.XPATH, '//*[@class = "col-md-12"]')
        guidebook_title = mainbody.find_element(By.TAG_NAME, 'h1').text
        crag_tables = self.driver.find_elements(By.XPATH, '//*[@class = "col-sm-6"]')
        if len(crag_tables) > 0:
            rows = []
            headers = []
            for table in crag_tables:
                rows = rows + table.find_elements(By.TAG_NAME, "tr")
                headers = headers + table.find_elements(By.CLASS_NAME, 'hdr1')
            crag_rows = [x for x in rows if x not in headers] #Remove headers from rows
            crags = {}
            for idx, row in enumerate(crag_rows):
                    a_tag = row.find_element(By.TAG_NAME, 'a')
                    crag_url = a_tag.get_attribute('href')
                    crag_uid = crag_url.split('=')[-1]
                    crag_name = a_tag.text
                    crag_rocktype = row.find_element(By.XPATH, './td[3]').text
                    crags[(f"crag:{idx}")] = {"crag_uid":crag_uid,"crag_name":crag_name,"crag_URL":crag_url,"rocktype":crag_rocktype, "guidebook":guidebook_title,"guidebook_URL":guidebook_URL}
            return(crags)
        else:   
            print(f"no crags in guidebook: {guidebook_title}")
            return({})

    def get_routes(self,crag,database_engine,check_db):
        """
        scrapes the crag page for all the routes and returns a dictionary of buttresses which contain a dictionary of every route at the buttress
        """
        crag_URL = crag["crag_URL"]
        self.driver.get(crag_URL)
        table = self.driver.find_element(By.ID, 'climb_table')
        table_body = table.find_element(By.TAG_NAME, 'tbody')
        table_rows = table_body.find_elements(By.TAG_NAME, 'tr')
        buttress_list = table_body.find_elements(By.XPATH, './/tr[@class ="dtrg-group buttress_header dtrg-start dtrg-level-0"]')
        routes_dict = {}
        num_route = 0
        for row in table_rows:
            if row in buttress_list:
                buttress = row.find_element(By.TAG_NAME, 'h5').text
            elif row not in buttress_list:
                a_tag = row.find_element(By.XPATH, './/*[@class = "small not-small-md main_link "]')
                route_URL = a_tag.get_attribute('href')
                route_uid = route_URL.split('-')[-1]
                if database_engine.isin_database(route_uid,"route_uid") == False or check_db == False:
                    route_name = a_tag.text
                    climbing_type= row.find_element(By.XPATH, './/td[@class = " datatable_column_type"]')
                    route_type = (climbing_type.find_element(By.TAG_NAME, 'i').get_attribute('title'))
                    grade = row.find_element(By.XPATH, './/td[@class = " datatable_column_grade small not-small-md"]')
                    route_grade = grade.find_element(By.TAG_NAME, "span").text
                    stars= row.find_element(By.XPATH, './/td[@class = " datatable_column_star"]')
                    try:    
                        route_stars = stars.find_element(By.TAG_NAME, 'i').get_attribute('title')    
                    except:
                        route_stars = "None"
                    num_route += 1
                    routes_dict[f"route:{num_route}"] = {"route_uid":route_uid,"name":route_name,"URL":route_URL,"type":route_type,"grade":route_grade,"stars":route_stars,"buttress":buttress}
                #else:
                    #print(f"Route with uid:{route_uid}, Already in database")
            else:
                print("what is this row????")
        return(routes_dict)

    def get_cragPics(self,crag,image_storage,check_db):
        """
        scrapes the crag page for all the photos, gets there title and the high quality image source. returns a dictionary of images where each photo has a v4 UUID
        """
        crag_URL = crag["crag_URL"]
        crag_uid = crag["crag_uid"]
        self.driver.get(crag_URL)
        pics_tab = self.driver.find_element(By.ID, 'show_photos').get_attribute('href')
        self.driver.get(pics_tab)
        self.driver.refresh()
        time.sleep(1)
        photos_list = self.driver.find_elements(By.XPATH, '//a[@class = "photoswipe"]')
        images = {}
        image_count = 0
        for photo in photos_list:
            img_thumbnail = photo.find_element(By.CLASS_NAME, 'img-fluid')
            title = (img_thumbnail.get_attribute('alt')).split('<',1)[0]
            object_name = "{}:Crag#{}".format(title,crag_uid).replace(","," ")
            object_name = object_name.replace(" ","_")
            if image_storage.isin_s3(object_name) != "object does exist" or check_db == False:
                photo_src = photo.get_attribute('data-image')
                images[f"image:{image_count}"] = {"title":title, "source":photo_src,"s3_object_name":object_name}
                image_count += 1
            #else:
               #print(f"image {title} already exists in s3")
        return(images)
    
    def save_dictionary(self, dictionary, name):
        """
        Saves the input dictionary as a .json file with the input name
        """
        with open(f"{name}.json", "w") as write_file:   
            json.dump(dictionary, write_file, indent=6)



if __name__ == "__main__":
    
    eng_climbs = scraper()
    if eng_climbs.load_and_accept_cookies(headless = True) == "Cookies Accepted":
        eng_climbs.guidebooks = eng_climbs.get_guidebooks("England")
        ukc_database = uploadto_aws.aws_client("ukc-data")
        UploadToDB = True
        # for guidebook in  eng_climbs.guidebooks:
        for index in range(3,4):
            guidebook = eng_climbs.guidebooks[index]
            crags_dict = eng_climbs.get_crags(guidebook)
            crag_list = list(crags_dict.keys())
            for crag in crag_list:
                print(crags_dict[crag]["crag_name"])
                climbs_dict = eng_climbs.get_routes(crags_dict[crag],ukc_database,UploadToDB)
                crags_dict[crag]["climbs"] = climbs_dict
                if len(climbs_dict) > 0 and UploadToDB == True:
                    ukc_database.create_dataframe(crags_dict[crag],upload=True)
                else:
                    print("Upload turned off or no climbs from crag, may already be in database")
                image_dict = eng_climbs.get_cragPics(crags_dict[crag],ukc_database,UploadToDB)
                crags_dict[crag]["images"] = image_dict
                if len(image_dict) > 0 and UploadToDB == True:
                    ukc_database.upload_images_s3(image_dict)
                else:
                    print("all images from crag already in s3")
    else:
        print("ERROR Accepting Cookies")



    

    