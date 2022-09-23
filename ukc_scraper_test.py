from doctest import Example
from ukc_scraper import scraper
from hypothesis import example, given, strategies as st
import unittest


class TestScraper(unittest.TestCase):
    def test_accept_cookies(self):
        actual_value = self.test_scraper.load_and_accept_cookies()
        expected_value = "Cookies Accepted"
        self.assertEqual(expected_value,actual_value)

    def setUp(self):
        self.test_scraper = scraper()
        self.test_scraper.load_and_accept_cookies()
    
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

    def test_get_crags(self):
        actual_value = self.test_scraper.get_crags("https://www.ukclimbing.com/logbook/books/baggy_climbing_guide-62")
        expected_value = {}
        self.assertEqual(expected_value,actual_value)


if __name__ == "__main__":

    unittest.main()



    
    # if type(test.get_crags("https://www.ukclimbing.com/logbook/books/baggy_climbing_guide-62")) == list: #test 4 to see if no crags exist in guide book (input is guidebook with no crags)
    #     test_failed.append(True)
    #     print("test 4 failed")
    # crag = test.get_crags(guidebooks[0])
    # if type(crag) != dict: #test 5 to see if correct output is recieved
    #     if type(crag[0]) != list:
    #         test_failed.append(True)
    #         print("test 5 failed")
    # first_crag = list(crag.keys())[0]
    # if type(test.get_routes(crag[first_crag])) != dict: #test 6 to see if correct output is recieved
    #     test_failed.append(True)
    #     print("test 6 failed")
    # if type(test.get_cragPics(crag[first_crag])) != dict: #test 7 to see if correct output is recieved
    #     test_failed.append(True)
    #     print("test 7 failed")
    
    # print(f"testing complete: {len(test_failed)} failed tests")