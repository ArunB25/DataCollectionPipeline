import ukc_scraper
import hypothesis
import unittest


class TestScraper(unittest.TestCase):
    def test_get_guidebooks(self):
        
    


if __name__ == "__main__":


    test = ukc_scraper.scraper()
    test.load_and_accept_cookies()
    test_failed = []
    if type(test.get_guidebooks("")) == list: #test 1 if nothing is inputed for country
        test_failed.append(True)
        print("test 1 failed")
    if type(test.get_guidebooks("asafnknflsad")) == list: #test 2 if country doesnt exist
        test_failed.append(True)
        print("test 2 failed")
    guidebooks = test.get_guidebooks("England") 
    if type(guidebooks) != list: #test 3 to see if correct output is recieved
        test_failed.append(True)
        print("test 3 failed")
    if type(test.get_crags("https://www.ukclimbing.com/logbook/books/baggy_climbing_guide-62")) == list: #test 4 to see if no crags exist in guide book (input is guidebook with no crags)
        test_failed.append(True)
        print("test 4 failed")
    crag = test.get_crags(guidebooks[0])
    if type(crag) != dict: #test 5 to see if correct output is recieved
        if type(crag[0]) != list:
            test_failed.append(True)
            print("test 5 failed")
    first_crag = list(crag.keys())[0]
    if type(test.get_routes(crag[first_crag])) != dict: #test 6 to see if correct output is recieved
        test_failed.append(True)
        print("test 6 failed")
    if type(test.get_cragPics(crag[first_crag])) != dict: #test 7 to see if correct output is recieved
        test_failed.append(True)
        print("test 7 failed")
    
    print(f"testing complete: {len(test_failed)} failed tests")