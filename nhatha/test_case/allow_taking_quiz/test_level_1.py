import pytest
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ddt import ddt, data, unpack
import sys

sys.path.insert(1, "C:\\Users\\ADMIN\\University\\222_ST\\Software-Testing\\nhatha\\test_case\\utility")
import utils
import logging


@pytest.fixture(scope="module")
def get_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return options


@pytest.fixture(autouse=True, scope="class")
def home(get_options):
    driver = webdriver.Chrome(options=get_options)
    driver.get("https://school.moodledemo.net/")
    TestLevel1.page = driver
    yield
    # yield driver
    driver.quit()


class Setup:
    @staticmethod
    def set_time(page, type, keys):
        # logging.info(keys)
        page.find_element(By.XPATH, '//*[@id="id_time{}_enabled"]'.format(type)).click()
        page.find_element(By.XPATH, '//*[@id="id_time{}_day"]'.format(type)).send_keys(keys.day)
        page.find_element(By.XPATH, '//*[@id="id_time{}_month"]'.format(type)).send_keys(keys.strftime("%B"))
        page.find_element(By.XPATH, '//*[@id="id_time{}_year"]'.format(type)).send_keys(keys.year)
        page.find_element(By.XPATH, '//*[@id="id_time{}_hour"]'.format(type)).send_keys(keys.hour)
        page.find_element(By.XPATH, '//*[@id="id_time{}_minute"]'.format(type)).send_keys(keys.minute)

    @staticmethod
    def login(page, name, password):
        # click login
        page.find_element(By.PARTIAL_LINK_TEXT, "Log in").click()
        # clear old data
        page.find_element(By.XPATH, '//*[@id="username"]').clear()
        page.find_element(By.XPATH, '//*[@id="password"]').clear()
        # send new data
        page.find_element(By.XPATH, '//*[@id="username"]').send_keys(name)
        page.find_element(By.XPATH, '//*[@id="password"]').send_keys(password + Keys.ENTER)

    @staticmethod
    def setup_quiz(page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        # login as teacher
        Setup.login(page, "teacher", "moodle")
        el = WebDriverWait(page, timeout=3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, course_name)))
        el.click()

        # enter edit mode
        page.find_element(By.XPATH, '//*[@id="usernavigation"]/form/div/div').click()
        # add activity
        el = WebDriverWait(page, timeout=3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="coursecontentcollapse0"]/button/span[2]')))
        el.click()
        # choose quiz
        el = WebDriverWait(page, timeout=3).until(EC.presence_of_element_located((By.XPATH, '//a[@title="Add a new Quiz"]')))
        el.click()

        # set quiz name
        page.find_element(By.XPATH, '//*[@id="id_name"]').send_keys(quiz_name)
        page.find_element(By.XPATH, '//*[@id="collapseElement-1"]').click()

        # set open time
        Setup.set_time(page, "open", open_date)
        # set close time
        Setup.set_time(page, "close", close_date)
        # set maximum attempt = 1
        page.find_element(By.XPATH, '//*[@id="collapseElement-2"]').click()
        page.find_element(By.XPATH, ' //*[@id="id_attempts"]').send_keys(1)
        # set restriction
        if not restriction == "None":
            el = WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="collapseElement-11"]')))
            el.click()
            el = WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.availability-button button")))
            el.click()
            # page.find_element(By.XPATH, '//button[text()="Add restriction..."]').click()
            page.find_element(By.XPATH, "//*[@id='availability_addrestriction_profile']").click()
            page.find_element(By.XPATH, '//span[text()="User profile field"]/following-sibling::select').send_keys("Email address")
            page.find_element(By.XPATH, '//span[text()="Value to compare against"]/following-sibling::input').send_keys(restriction)
        # save setting
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_submitbutton"]'))).click()

        # add questions
        page.find_element(By.PARTIAL_LINK_TEXT, "Questions").click()
        el = WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="action-menu-toggle-1"]')))
        el.click()
        el = WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="action-menu-1-menu"]/a[2]')))
        el.click()
        # select questions
        el = WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qbheadercheckbox"]')))
        el.click()
        page.find_element(By.CSS_SELECTOR, "div.pt-2 input").click()
        # logout
        page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[10]").click()

    @staticmethod
    def access_course(page, course_name):
        Setup.login(page, "student", "moodle")
        el = WebDriverWait(page, timeout=3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, course_name)))
        el.click()

    @staticmethod
    def access_quiz(page, quiz_name):
        el = WebDriverWait(page, timeout=3).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, quiz_name)))
        el.click()
        # logging.info(page.title)

    @staticmethod
    def attempt(page):
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Attempt quiz"]'))).click()
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Finish attempt ..."))).click()
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Submit all and finish"]'))).click()
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.modal-footer button:nth-child(2)"))).click()
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Finish review"))).click()


@ddt
class TestLevel1(unittest.TestCase):
    page = None

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_1"))
    @unpack
    def test_1(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        Setup.access_quiz(self.page, quiz_name)
        assert quiz_name in self.page.title
        assert len(self.page.find_elements(By.XPATH, '//button[text()="Attempt quiz"]')) == 0
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_2"))
    @unpack
    def test_2(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        Setup.access_quiz(self.page, quiz_name)
        assert quiz_name in self.page.title
        assert len(self.page.find_elements(By.XPATH, '//button[text()="Attempt quiz"]')) == 0
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_3"))
    @unpack
    def test_3(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        assert len(self.page.find_elements(By.PARTIAL_LINK_TEXT, quiz_name)) == 0
        assert "Not available unless: Your <strong>Email address</strong> is <strong>{}</strong>".format(restriction) in self.page.page_source
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_4"))
    @unpack
    def test_4(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        Setup.access_quiz(self.page, quiz_name)
        Setup.attempt(self.page)
        assert "No more attempts are allowed" in self.page.page_source
        assert len(self.page.find_elements(By.XPATH, '//button[text()="Attempt quiz"]')) == 0
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_5"))
    @unpack
    def test_5(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        Setup.access_quiz(self.page, quiz_name)
        assert (
            WebDriverWait(self.page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Attempt quiz"]'))).is_displayed()
            == True
        )
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_6"))
    @unpack
    def test_6(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        assert len(self.page.find_elements(By.PARTIAL_LINK_TEXT, quiz_name)) == 0
        assert "Not available unless: Your <strong>Email address</strong> is <strong>{}</strong>".format(restriction) in self.page.page_source
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_7"))
    @unpack
    def test_7(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        Setup.access_quiz(self.page, quiz_name)
        assert quiz_name in self.page.title
        assert len(self.page.find_elements(By.XPATH, '//button[text()="Attempt quiz"]')) == 0
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()

    @data(*utils.Utility.read_data_from_excel("..\\test_data\\allow_taking_quiz.xlsx", "Testcase_8"))
    @unpack
    def test_8(self, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction):
        Setup.setup_quiz(self.page, course_name, quiz_name, open_date, close_date, out_of_attempt, restriction)
        Setup.access_course(self.page, course_name)
        assert len(self.page.find_elements(By.PARTIAL_LINK_TEXT, quiz_name)) == 0
        assert "Not available unless: Your <strong>Email address</strong> is <strong>{}</strong>".format(restriction) in self.page.page_source
        # logout
        self.page.find_element(By.XPATH, "//*[@id='user-menu-toggle']").click()
        self.page.find_element(By.XPATH, "//*[@id='carousel-item-main']/a[9]").click()
