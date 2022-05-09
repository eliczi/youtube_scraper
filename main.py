from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

path = "C:\\Users\Adam\Documents\GitHub\youtube_scraper\chromedriver.exe"
video = "https://www.youtube.com/watch?v=U6gbGk5WPws"
driver = webdriver.Chrome(path)
driver.get(video)
driver.implicitly_wait(10)
x = driver.find_element(by=By.CSS_SELECTOR,
                        value="[aria-label='Accept the use of cookies and other data for the purposes described']")
x.click()
button = driver.find_element(by=By.CLASS_NAME, value='ytp-ad-skip-button-container')
button.click()
x = driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Skip trial']")
x.click()


def scroll_to_bottom():
    page_eng = False
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while not page_eng:
        driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
        time.sleep(1)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if last_height == new_height:
            page_eng = True
        else:
            last_height = new_height


def scroll_num_times(num):
    for _ in range(num):
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        time.sleep(1)
