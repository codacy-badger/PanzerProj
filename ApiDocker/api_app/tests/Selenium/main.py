import time
import unittest
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class FitnessBrowser:
    def __init__(self):
        # logger setup`s
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('FitnessPersonalArea')

        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument("--window-size=1920x1080")
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(chrome_options = chrome_options)
        self.driver.implicitly_wait(4)

    def __del__(self):
        self.driver.quit()

