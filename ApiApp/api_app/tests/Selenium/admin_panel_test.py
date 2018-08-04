import time
import unittest
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from .main import FitnessBrowser


class AdminSearchTest(unittest.TestCase):
    """
    Тестирует поиск в таблицах через панель администрации
    """
    def setUp(self):

        self.logger = FitnessBrowser().logger
        formatter = FitnessBrowser().formatter
        # create file handler which logs even debug messages
        search_tests = logging.FileHandler('logs/AdminSearchTest.log')
        search_tests.setFormatter(formatter)
        self.logger.addHandler(search_tests)

        self.driver = FitnessBrowser().driver
        # start admin page
        self.driver.get('http://localhost:8080/admin/login/?next=/admin/')

        # base url
        self.base_url = 'http://localhost:8080/'

        # admin login data
        self.admin_login = 'drang'
        self.admin_password = 'Qq7729702'

        # tables amount
        self.tables_amount = 27

        # RU title
        self.ru_title = 'Административный сайт Django'
        # EN title
        self.en_title = 'Django site admin'

    # login in admin panel
    def login_in_panel(self):
        self.driver.find_element_by_id('id_username').send_keys(self.admin_login)
        self.driver.find_element_by_id('id_password').send_keys(self.admin_password)
        self.driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').submit()

    # test admin login
    def test_admin_login(self):
        # test title
        assert self.ru_title in self.driver.title

        self.login_in_panel()

        # test title
        assert self.ru_title in self.driver.title

    # test personal area models list
    def test_personal_area_models(self):
        self.login_in_panel()

        # get personal area model
        model_title = self.driver.find_element_by_xpath('//*[@id="content-main"]/div[1]/table/caption/a')

        assert 'Fitness Personal Area' in model_title.get_attribute('text')

        # open fitness area model page
        self.driver.get(model_title.get_attribute('href'))

        assert 'Администрирование приложения «Fitness Personal Area»' in self.driver.title

        # get tables href`s
        model_tables_hrefs = [href.get_attribute('href') for href in self.driver.find_elements_by_xpath('//tr/th/a')]

        # check tables amount
        assert len(model_tables_hrefs) == self.tables_amount

        for href in model_tables_hrefs:
            self.driver.get(href)

            try:
                self.driver.find_element_by_id('searchbar').send_keys('Some search')
                self.driver.find_element_by_xpath('//*[@id="changelist-search"]/div/input[2]').submit()

                assert 'FieldError' not in self.driver.title

            except NoSuchElementException:
                self.logger.info(f'Test: [test_personal_area_models]; HREF: {href}; Info: No search bar.')


class AdminElementsCreating(unittest.TestCase):
    """
    Тестирует создание новых элементов через панель администрации
    """
    def setUp(self):

        self.logger = FitnessBrowser().logger
        formatter = FitnessBrowser().formatter
        # create file handler which logs even debug messages
        creating_tests = logging.FileHandler('logs/AdminElementsCreating.log')
        creating_tests.setFormatter(formatter)
        self.logger.addHandler(creating_tests)

        self.driver = FitnessBrowser().driver
        # start admin page
        self.driver.get('http://localhost:8080/admin/login/?next=/admin/')

        # base url
        self.base_url = 'http://localhost:8080/'

        # admin login data
        self.admin_login = 'drang'
        self.admin_password = 'Qq7729702'

    # login in admin panel
    def login_in_panel(self):
        self.driver.find_element_by_id('id_username').send_keys(self.admin_login)
        self.driver.find_element_by_id('id_password').send_keys(self.admin_password)
        self.driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/input').submit()

    def test_body_parameter_creating(self):
        BODY_TITLE = 'TEST body title'
        BODY_DATA = '666,0'

        self.login_in_panel()
        self.driver.get('http://localhost:8080/admin/FitnessPersonalArea/bodyparameter/')

        assert 'body parameter' in self.driver.title
        self.driver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()

        assert 'body parameter' in self.driver.title

        # fill body_parameter form
        self.driver.find_element_by_xpath('//*[@id="id_user"]/option[2]').click()
        self.driver.find_element_by_id('id_body_title').send_keys(BODY_TITLE)
        self.driver.find_element_by_id('id_body_data').send_keys(BODY_DATA)
        self.driver.find_element_by_xpath('//*[@id="bodyparameter_form"]/div/div/input[1]').submit()

        assert 'body parameter' in self.driver.title

        body_title = self.driver.find_element_by_xpath('//tbody/tr[1]/td[2]').text
        body_data = self.driver.find_element_by_xpath('//tbody/tr[1]/td[3]').text

        assert BODY_DATA == body_data
        assert BODY_TITLE == body_title

    def test_chat_message_creating(self):
        MESSAGE_TEXT = 'TEST MESSAGE TEXT'

        self.login_in_panel()
        self.driver.get('http://localhost:8080/admin/FitnessPersonalArea/chatmessage/')

        assert 'chat message' in self.driver.title
        self.driver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()

        assert 'chat message' in self.driver.title

        # fill chat_message form
        self.driver.find_element_by_xpath('//*[@id="id_user"]/option[2]').click()
        self.driver.find_element_by_xpath('//*[@id="id_message_chat"]/option[2]').click()
        self.driver.find_element_by_id('id_message_text').send_keys(MESSAGE_TEXT)
        self.driver.find_element_by_xpath('//*[@id="chatmessage_form"]/div/div/input[1]').submit()

        assert 'chat message' in self.driver.title

        message_text = self.driver.find_element_by_xpath('//tbody/tr/td[2]').text

        assert MESSAGE_TEXT == message_text


if __name__ == "__main__":
    unittest.main()
