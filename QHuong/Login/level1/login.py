import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas
import openpyxl

service = Service('../../chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)

df = pandas.read_excel('Testcases.xlsx', sheet_name='Testcases', converters={'Password':str, 'Username':str, 'Result':str})

# save data as an array
TEST_DATA = df.to_numpy()

def test_1():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[0][0]) is float else TEST_DATA[0][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[0][1]) is float else TEST_DATA[0][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[0][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_2():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[1][0]) is float else TEST_DATA[1][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[1][1]) is float else TEST_DATA[1][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[1][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_3():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[2][0]) is float else TEST_DATA[2][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[2][1]) is float else TEST_DATA[2][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[2][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_4():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[3][0]) is float else TEST_DATA[3][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[3][1]) is float else TEST_DATA[3][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[3][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_5():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[4][0]) is float else TEST_DATA[4][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[4][1]) is float else TEST_DATA[4][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[4][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_6():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[5][0]) is float else TEST_DATA[5][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[5][1]) is float else TEST_DATA[5][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[5][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_7():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[6][0]) is float else TEST_DATA[6][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[6][1]) is float else TEST_DATA[6][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[6][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_8():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[7][0]) is float else TEST_DATA[7][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[7][1]) is float else TEST_DATA[7][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[7][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    
    
def test_9():
    
    driver.get("https://school.moodledemo.net/login/index.php")
    driver.maximize_window()
    element = driver.find_element(By.ID, "username")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[8][0]) is float else TEST_DATA[8][0])
    time.sleep(1)
    
    element = driver.find_element(By.ID, "password")
    element.clear()      
    element.send_keys('' if type(TEST_DATA[8][1]) is float else TEST_DATA[8][1])
    time.sleep(1)
    
    driver.find_element(By.ID, "loginbtn").click()
    
    if(TEST_DATA[8][2] == 'fail'):
        assert driver.find_element(By.CSS_SELECTOR, ".alert").text == "Invalid login, please try again"

    