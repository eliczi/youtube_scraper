from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

path = "C:\\Users\Adam\Documents\GitHub\youtube_scraper\chromedriver.exe"
video = "https://www.youtube.com/watch?v=bSCsmBkGzc4"
driver = webdriver.Chrome(path)
driver.get(video)
driver.implicitly_wait(25)
x = driver.find_element(by=By.CSS_SELECTOR,
                        value="[aria-label='Accept the use of cookies and other data for the purposes described']")
x.click()


# button = driver.find_element(by=By.CLASS_NAME, value='ytp-ad-skip-button-container')
# button.click()
# x = driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Skip trial']")
# x.click()
#

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


scroll_to_bottom()
data = []
likes = []

for comment in WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, "content-text"))):
    data.append(comment.text)

# likes = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')
# for like in likes:
#     x = ''
#     if like.text == '':
#         x = 0
#     else:
#         if 'K' in like.text:
#             x = like.text.replace('K', '')
#             x = float(x) * 1000
#             x = int(x)
#         else:
#             x = int(like.text)
#     likes.append(x)


author = driver.find_elements_by_id('author-text')
df = pd.DataFrame(data)
df.to_csv('data.csv', sep=',', index=False)