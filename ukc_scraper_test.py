#from doctest import Example
from ukc_scraper import scraper
import uploadto_aws
import unittest
import json


class TestScraper(unittest.TestCase):
    def test_accept_cookies(self):
        actual_value = self.test_scraper.load_and_accept_cookies(headless = True)
        expected_value = "Cookies Accepted"
        self.assertEqual(expected_value,actual_value)
        
    def setUp(self):
        self.test_scraper = scraper()
        self.test_scraper.load_and_accept_cookies(headless = True)
        self.ukc_database = uploadto_aws.aws_client("ukc-data")
    
    def test_get_guidebooks(self):
        expected_value = "invalid input"
        actual_value = self.test_scraper.get_guidebooks(" ")
        self.assertEqual(expected_value,actual_value)

        expected_value = "country not found"
        actual_value = self.test_scraper.get_guidebooks("ENG")
        self.assertEqual(expected_value,actual_value)

        expected_value = list
        actual_value = type(self.test_scraper.get_guidebooks("England"))
        self.assertEqual(expected_value,actual_value)

    def test_get_crags(self):
        actual_value = self.test_scraper.get_crags("https://www.ukclimbing.com/logbook/books/baggy_climbing_guide-62")
        expected_value = {}
        self.assertEqual(expected_value,actual_value)

        actual_value = list(self.test_scraper.get_crags("https://www.ukclimbing.com/logbook/books/a_climbers_guide_to_the_exmoor_coast_traverse-2237")["crag:0"])
        expected_value = ["crag_uid","crag_name","crag_URL","rocktype","guidebook","guidebook_URL"]
        self.assertEqual(expected_value,actual_value)

    def test_get_routes(self):
        first_crag = {"crag_URL":"https://www.ukclimbing.com/logbook/crags/the_exmoor_coast_traverse-1242/"}
        actual_value = self.test_scraper.get_routes(first_crag,self.ukc_database, check_db= False)["route:1"]
        expected_value = json.load(open("first_crag.json"))["crag:0"]["climbs"]["route:1"]
        self.assertEqual(expected_value,actual_value)

    def test_get_images(self):
        first_crag = {"crag_URL":"https://www.ukclimbing.com/logbook/crags/the_exmoor_coast_traverse-1242/","crag_uid":"1242"}
        actual_value = self.test_scraper.get_cragPics(first_crag,self.ukc_database, check_db= False)["image:0"]
        expected_value = json.load(open("first_crag.json"))["crag:0"]["images"]["image:0"]
        self.assertEqual(expected_value,actual_value)



if __name__ == "__main__":

    unittest.main()
