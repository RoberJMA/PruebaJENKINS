from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_example(self):
        driver = self.driver
        driver.get("http://localhost:30080")  # URL de la aplicación desplegada
        self.assertIn("phpMyAdmin", driver.title)
        elem = driver.find_element(By.NAME, "pma_username")
        elem.send_keys("root")
        elem = driver.find_element(By.NAME, "pma_password")
        elem.send_keys("root")
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        self.assertIn("phpMyAdmin", driver.title)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
