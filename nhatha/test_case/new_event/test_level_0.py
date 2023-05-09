import datetime
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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
    TestLevel0.page = driver
    # yield
    yield driver
    driver.quit()


@pytest.fixture(autouse=True, scope="class")
def login(home):
    # click login
    home.find_element(By.PARTIAL_LINK_TEXT, "Log in").click()
    # clear old data
    home.find_element(By.XPATH, '//*[@id="username"]').clear()
    home.find_element(By.XPATH, '//*[@id="password"]').clear()
    # send new data
    home.find_element(By.XPATH, '//*[@id="username"]').send_keys("teacher")
    home.find_element(By.XPATH, '//*[@id="password"]').send_keys("moodle" + Keys.ENTER)
    time.sleep(4)
    home.find_element(By.XPATH, "//a[@role='menuitem'][normalize-space()='Dashboard']").click()


class Setup:
    @staticmethod
    def get_default_create_date(page):
        day = int(Select(page.find_element(By.XPATH, "//*[@id='id_timestart_day']")).first_selected_option.text)
        month = Select(page.find_element(By.XPATH, "//*[@id='id_timestart_month']")).first_selected_option.text
        month = datetime.datetime.strptime(month, "%B").month
        year = int(Select(page.find_element(By.XPATH, "//*[@id='id_timestart_year']")).first_selected_option.text)
        return datetime.date(year, month, day)

    @staticmethod
    def new_event(page):
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='New event']"))).click()
        time.sleep(4)

    @staticmethod
    def create_event_with_name(page, event_name):
        if event_name != "None":
            page.find_element(By.CSS_SELECTOR, "input#id_name").send_keys(event_name)
        date = Setup.get_default_create_date(page)
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))).click()
        return date

    @staticmethod
    def tear_down(page, event):
        event.click()
        time.sleep(2)
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.modal-footer button[data-action='delete']"))).click()
        time.sleep(2)
        delete_all = page.find_elements(By.CSS_SELECTOR, "div.modal-footer button[data-action='deleteall']")
        if len(delete_all) > 0:
            delete_all[0].click()
        else:
            WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete event']"))).click()
        time.sleep(2)

    @staticmethod
    def create_event_full(page, event_name: str, create_date: datetime.datetime, end_date: datetime.datetime | str | int, repeat: bool | int):
        # name
        page.find_element(By.CSS_SELECTOR, "input#id_name").send_keys(event_name)
        # create_date
        page.find_element(By.XPATH, "//select[@id='id_timestart_day']").send_keys(create_date.day)
        page.find_element(By.XPATH, "//select[@id='id_timestart_month']").send_keys(create_date.strftime("%B"))
        page.find_element(By.XPATH, "//select[@id='id_timestart_year']").send_keys(create_date.year)
        page.find_element(By.XPATH, "//select[@id='id_timestart_hour']").send_keys(create_date.hour)
        page.find_element(By.XPATH, "//select[@id='id_timestart_minute']").send_keys(create_date.minute)

        # click show more
        page.find_element(By.XPATH, "//a[normalize-space()='Show more...']").click()
        time.sleep(3)

        # end_date
        if type(end_date) is str:
            page.find_element(By.CSS_SELECTOR, "#id_duration_0").click()
        elif type(end_date) is datetime.datetime:
            page.find_element(By.CSS_SELECTOR, "#id_duration_1").click()
            page.find_element(By.CSS_SELECTOR, "#id_timedurationuntil_day").send_keys(end_date.day)
            page.find_element(By.CSS_SELECTOR, "#id_timedurationuntil_month").send_keys(end_date.strftime("%B"))
            page.find_element(By.CSS_SELECTOR, "#id_timedurationuntil_year").send_keys(end_date.year)
            page.find_element(By.CSS_SELECTOR, "#id_timedurationuntil_hour").send_keys(end_date.hour)
            page.find_element(By.CSS_SELECTOR, "#id_timedurationuntil_minute").send_keys(end_date.minute)
        else:
            page.find_element(By.CSS_SELECTOR, "#id_duration_2").click()
            page.find_element(By.CSS_SELECTOR, "#id_timedurationminutes").clear()
            page.find_element(By.CSS_SELECTOR, "#id_timedurationminutes").send_keys(end_date)

        # repeat
        if type(repeat) is int:
            page.find_element(By.CSS_SELECTOR, "#id_repeat").click()
            page.find_element(By.CSS_SELECTOR, "#id_repeats").clear()
            page.find_element(By.CSS_SELECTOR, "#id_repeats").send_keys(repeat)

        # click save
        WebDriverWait(page, timeout=10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))).click()
        return datetime.date(create_date.year, create_date.month, create_date.day)


class TestLevel0:
    page = None

    def get_current_date(self, create_date):
        calendar = self.page.find_element(By.CSS_SELECTOR, "div.calendarwrapper")
        current_month = int(calendar.get_attribute("data-month"))
        current_year = int(calendar.get_attribute("data-year"))
        current = datetime.date(current_year, current_month, create_date.day)
        return current

    def verify_event_is_created(self, event_title, create_date):
        current = self.get_current_date(create_date)
        time.sleep(3)
        if current > create_date:
            while current != create_date:
                WebDriverWait(
                    self.page,
                    timeout=3,
                ).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Previous month']"))).click()
                time.sleep(2)
                current = self.get_current_date(create_date)
                time.sleep(3)
        elif current < create_date:
            while current != create_date:
                WebDriverWait(self.page, timeout=3).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Next month']"))).click()
                time.sleep(2)
                current = self.get_current_date(create_date)
                time.sleep(3)

        event = WebDriverWait(self.page, timeout=3).until(
            EC.element_to_be_clickable((By.XPATH, "//td[@data-day='{}']//a[@title='{}']".format(create_date.day, event_title)))
        )
        assert event.is_displayed() == True
        return event

    def test_1(self):
        event_name = "Kiểm tra X"
        Setup.new_event(self.page)
        date = Setup.create_event_with_name(self.page, event_name)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_2(self):
        event_name = "X"
        Setup.new_event(self.page)
        date = Setup.create_event_with_name(self.page, event_name)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_3(self):
        event_name = "XX"
        Setup.new_event(self.page)
        date = Setup.create_event_with_name(self.page, event_name)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_4(self):
        event_name = "None"
        Setup.new_event(self.page)
        Setup.create_event_with_name(self.page, event_name)
        name_field = self.page.find_element(By.XPATH, "//div[@id='fitem_id_name']")
        error = name_field.find_elements(By.CSS_SELECTOR, "div#id_error_name")
        assert len(error) > 0

    def test_5(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 30)
        end_date = datetime.datetime(2023, 4, 10, 0, 30)
        repeat = False
        Setup.new_event(self.page)
        date = Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_6(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 30)
        end_date = datetime.datetime(2023, 4, 9, 0, 30)
        repeat = False
        Setup.new_event(self.page)
        date = Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_7(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 30)
        end_date = "Without Duration"
        repeat = 0
        Setup.new_event(self.page)
        date = Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_8(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 30)
        end_date = 30
        repeat = -1
        Setup.new_event(self.page)
        Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        repeat_field = self.page.find_element(By.CSS_SELECTOR, "#fitem_id_repeats")
        error = repeat_field.find_elements(By.CSS_SELECTOR, "div#id_error_repeat")
        assert len(error) > 0

    def test_9(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 30)
        end_date = datetime.datetime(2023, 4, 8, 0, 30)
        repeat = False
        Setup.new_event(self.page)
        Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        duration_field = self.page.find_element(By.CSS_SELECTOR, "#fgroup_id_durationgroup")
        error = duration_field.find_elements(By.CSS_SELECTOR, "#fgroup_id_error_durationgroup")
        assert len(error) > 0

    def test_10(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 30)
        end_date = datetime.datetime(2023, 4, 9, 0, 25)
        repeat = False
        Setup.new_event(self.page)
        Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        duration_field = self.page.find_element(By.CSS_SELECTOR, "#fgroup_id_durationgroup")
        error = duration_field.find_elements(By.CSS_SELECTOR, "#fgroup_id_error_durationgroup")
        assert len(error) > 0

    def test_11(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 25)
        end_date = 0
        repeat = 0
        Setup.new_event(self.page)
        Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        duration_field = self.page.find_element(By.CSS_SELECTOR, "#fgroup_id_durationgroup")
        error = duration_field.find_elements(By.CSS_SELECTOR, "#fgroup_id_error_durationgroup")
        assert len(error) > 0

    def test_12(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 25)
        end_date = "Without Duration"
        repeat = 1
        Setup.new_event(self.page)
        Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        name_field = self.page.find_element(By.XPATH, "//div[@id='fitem_id_name']")
        error = name_field.find_elements(By.CSS_SELECTOR, "div#id_error_name")
        assert len(error) > 0

    def test_13(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 25)
        end_date = datetime.datetime(2023, 4, 10, 0, 30)
        repeat = -1
        Setup.new_event(self.page)
        Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        repeat_field = self.page.find_element(By.CSS_SELECTOR, "#fitem_id_repeats")
        error = repeat_field.find_elements(By.CSS_SELECTOR, "div#id_error_repeat")
        assert len(error) > 0

    def test_14(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 25)
        end_date = 30
        repeat = 1
        Setup.new_event(self.page)
        date = Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)

    def test_15(self):
        event_name = "X"
        create_date = datetime.datetime(2023, 4, 9, 0, 25)
        end_date = "Without Duration"
        repeat = 3
        Setup.new_event(self.page)
        date = Setup.create_event_full(self.page, event_name, create_date, end_date, repeat)
        event = self.verify_event_is_created(event_name, date)
        Setup.tear_down(self.page, event)
