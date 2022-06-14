from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


class YouTubeScraper:
    def __init__(self, video, sort_by='top'):
        self.sort_by = sort_by
        self.video = video
        # self.path = "C:\\Users\Adam\Documents\GitHub\youtube_scraper\chromedriver.exe"
        # self.driver = webdriver.Chrome(self.path)
        self.driver = webdriver.Chrome()
        self.comments = {'comments': [],
                         'likes': [],
                         'username': [],
                         'date': [],
                         'replies': [],
                         'channel': []}
        self.df = None

    def scrape(self):
        self.driver.get(self.video)
        #self.driver.implicitly_wait(1)
        self.accept_cookies()
        self.scroll_to_bottom()
        self.extract_comments()
        self.comments.pop('replies', None)
        self.df = pd.DataFrame(self.comments)
        self.df.to_csv('df.csv')

    def change_comments_sorting(self):
        if self.sort_by != 'top':
            sort = self.driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Sort comments']")
            self.driver.execute_script("arguments[0].scrollIntoView();", sort)
            self.driver.execute_script("arguments[0].click();", sort)

    def extract_comments(self):
        main_comments = self.driver.find_elements(by=By.CSS_SELECTOR, value='ytd-comment-thread-renderer')
        for main_comment in main_comments:
            text = main_comment.find_element(by=By.ID, value='content-text').text
            self.comments['comments'].append(text)
            likes = main_comment.find_element(by=By.ID, value='vote-count-middle')
            self.comments['likes'].append(likes.text)
            author = main_comment.find_element(by=By.ID, value='author-text')
            self.comments['username'].append(author.text)
            main_comment_channel = main_comment.find_element_by_id('author-text').get_attribute('href')
            self.comments['channel'].append(main_comment_channel)
            date = main_comment.find_element(by=By.CLASS_NAME, value='published-time-text')
            self.comments['date'].append(date.text)

            mc_replies = {'comments': [],  # main comment replies
                          'likes': [],
                          'username': [],
                          'date': [],
                          'replies': [],
                          'channel': []}

            replies = main_comment.find_element(by=By.ID, value='replies')
            # If there are any replies
            if replies.text != '':
                btn = replies.find_element(by=By.ID, value='button')
                self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                self.driver.execute_script("arguments[0].click();", btn)
                more_replies = main_comment.find_elements(by=By.CSS_SELECTOR, value="[aria-label='Show more replies']")
                # load more replies
                if len(more_replies) != 0:
                    self.driver.execute_script("arguments[0].click();", more_replies[0])
                    time.sleep(1)

                # ALl REPLIES
                replies = main_comment.find_element(by=By.ID, value='expander-contents')
                replies = main_comment.find_elements(by=By.ID, value='body')
                for i, r in enumerate(replies):
                    if i == 0:  # for some reason, the first reply is the original comment, so it is skipped
                        continue
                    text = r.find_element(by=By.ID, value='content-text').text
                    mc_replies['comments'].append(text)
                    likes = r.find_element(by=By.ID, value='vote-count-middle')
                    mc_replies['likes'].append(likes.text)
                    author = r.find_element(by=By.ID, value='author-text')
                    mc_replies['username'].append(author.text)
                    main_comment_channel = r.find_element(by=By.ID, value='author-text').get_attribute('href')
                    mc_replies['channel'].append(main_comment_channel)
                    date = r.find_element(by=By.CLASS_NAME, value='published-time-text')
                    mc_replies['date'].append(date.text)
                self.comments['replies'].append(mc_replies)
            else:
                self.comments['replies'].append(None)

    def accept_cookies(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Accept the use of cookies and other data for the purposes described']"))).click()

        # element = WebDriverWait(self.driver, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Accept the use of cookies and other data for the purposes described']"))
        # )
        #
        # # x = self.driver.find_element(by=By.CSS_SELECTOR,
        # #                              value="[aria-label='Accept the use of cookies and other data for the purposes described']")
        # element.click()
        # time.sleep(2)

    def skip_ad(self):
        button = self.driver.find_element(by=By.CLASS_NAME, value='ytp-ad-skip-button-container')
        button.click()

    def skip_trial(self):
        x = self.driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Skip trial']")
        x.click()

    def scroll_to_bottom(self):
        page_eng = False
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, 200)")  # initial scroll to load first comments
        time.sleep(1)
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
