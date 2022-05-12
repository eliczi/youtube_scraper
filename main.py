from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

path = "C:\\Users\Adam\Documents\GitHub\youtube_scraper\chromedriver.exe"


class YouTubeScraper:
    def __init__(self, video, sort_by='top'):
        self.sort_by = sort_by
        self.video = video
        self.driver = webdriver.Chrome(path)
        self.comments = {'comments': [],
                         'likes': [],
                         'username': [],
                         'date': [],
                         'replies': [],
                         'channel': []}

    def scrape(self):
        self.driver.get(self.video)
        self.driver.implicitly_wait(25)
        self.accept_cookies()
        # self.skip_ad()
        self.scroll_to_bottom()
        self.test()
        # self.view_more()
        # self.scrape_comments()
        # self.scrape_likes()
        # self.scrape_authors()
        # self.scrape_dates()
        # self.test()
        #print(self.comments)

    def test(self):
        main_comments = self.driver.find_elements(by=By.CSS_SELECTOR, value='ytd-comment-thread-renderer')
        for mc in main_comments:
            text = mc.find_element(by=By.ID, value='content-text').text
            self.comments['comments'].append(text)
            likes = mc.find_element(by=By.ID, value='vote-count-middle')
            self.comments['likes'].append(likes.text)
            author = mc.find_element(by=By.ID, value='author-text')
            self.comments['username'].append(author.text)
            main_comment_channel = mc.find_element_by_id('author-text').get_attribute('href')
            self.comments['channel'].append(main_comment_channel)
            date = mc.find_element(by=By.CLASS_NAME, value='published-time-text')
            self.comments['date'].append(date.text)

            repli = {'comments': [],
                       'likes': [],
                       'username': [],
                       'date': [],
                       'replies': [],
                       'channel': []}
            replies = mc.find_element(by=By.ID, value='replies')
            if replies.text != '':
                btn = replies.find_element(by=By.CLASS_NAME, value='ytd-button-renderer')
                time.sleep(1)
                btn.click()
                # btn.click()
            # print(replies)
            #replies = mc.find_element_by_xpath('..//*[@id="replies"]')  # get the replies section of the above comment
            # if replies.text.startswith('View'):  # check if there are any replies
            #     replies.find_element_by_css_selector('a').click()  # if so open the replies
            #     time.sleep(3)  # wait for load (better strategy should be used here
            #     # replies = mc.find_elements(by=By.CLASS_NAME, value='ytd-comment-replies-renderer')
                # print(len(replies))
                # for reply in replies.find_elements_by_id('author-text'):
                #     print(reply.text)
                #     #reply_channel = reply.get_attribute('href')
                #     #print('Reply channel: ' + reply_channel)  # print the channel of each reply

    def view_more(self):
        # id = more-replies
        button = self.driver.find_elements_by_xpath(
            '//*[contains(@class,"more-button style-scope ytd-comment-replies-renderer")]')
        print(button)
        button[0].click()

    def scrape_comments(self):
        for com in WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.ID, "content-text"))):
            self.comments['comments'].append(com.text)

    def scrape_authors(self):
        print('scraping authors')
        author = self.driver.find_elements_by_id('author-text')
        links = [elem.get_attribute('href') for elem in author]
        for link in links:
            self.comments['channel'].append(link)
        for au in author:
            self.comments['username'].append(au.text)

    def scrape_likes(self):
        print('scraping likes')
        likes = self.driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')
        for like in likes:
            x = ''
            if like.text == '':
                x = 0
            elif 'K' in like.text:
                x = like.text.replace('K', '')
                x = float(x) * 1000
                x = int(x)
            else:
                x = int(like.text)
            self.comments['likes'].append(x)

    def accept_cookies(self):
        x = self.driver.find_element(by=By.CSS_SELECTOR,
                                     value="[aria-label='Accept the use of cookies and other data for the purposes described']")
        x.click()

    def scrape_dates(self):

        button = self.driver.find_elements_by_xpath(
            '//*[contains(@class,"yt-simple-endpoint style-scope yt-formatted-string")]')
        for i in range(3, len(button)):
            self.comments['date'].append(button[i].text)

    def skip_ad(self):
        button = self.driver.find_element(by=By.CLASS_NAME, value='ytp-ad-skip-button-container')
        button.click()

    def skip_trial(self):
        x = self.driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Skip trial']")
        x.click()

    def scroll_to_bottom(self):
        page_eng = False
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while not page_eng:
            self.driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
            time.sleep(1)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if last_height == new_height:
                page_eng = True
            else:
                last_height = new_height

    def scroll_num_times(self, num):
        for _ in range(num):
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")
            time.sleep(1)


yt = YouTubeScraper('https://www.youtube.com/watch?v=Brz086XIUto')
yt.scrape()
