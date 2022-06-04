from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

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
        self.driver.implicitly_wait(2)
        self.accept_cookies()
        # self.skip_ad()
        # self.change_comments_sorting()
        self.scroll_to_bottom()
        self.test()
        # print(self.comments)

    def change_comments_sorting(self):
        if self.sort_by != 'top':
            sort = self.driver.find_elements(by=By.CSS_SELECTOR, value="[aria-label='Sort comments']")
            self.driver.execute_script("arguments[0].click();", sort[0])

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
                btn = replies.find_element(by=By.ID, value='button')
                self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                self.driver.execute_script("arguments[0].click();", btn)
                wd = mc.find_elements(by=By.CSS_SELECTOR, value="[aria-label='Show more replies']")
                if len(wd) != 0:
                    self.driver.execute_script("arguments[0].click();", wd[0])
                    time.sleep(1)
                replies = mc.find_element(by=By.ID, value='expander-contents')
                replies = mc.find_elements(by=By.ID, value='body')
                for i, r in enumerate(replies):
                    if i == 0:  # for some reason, the first reply is the original comment, so it is skipped
                        continue
                    text = r.find_element(by=By.ID, value='content-text').text
                    repli['comments'].append(text)
                    likes = r.find_element(by=By.ID, value='vote-count-middle')
                    repli['likes'].append(likes.text)
                    author = r.find_element(by=By.ID, value='author-text')
                    repli['username'].append(author.text)
                    main_comment_channel = r.find_element(by=By.ID, value='author-text').get_attribute('href')
                    # main_comment_channel = r.find_element_by_id('author-text').get_attribute('href')
                    repli['channel'].append(main_comment_channel)
                    date = r.find_element(by=By.CLASS_NAME, value='published-time-text')
                    repli['date'].append(date.text)
                self.comments['replies'].append(repli)
            else:
                self.comments['replies'].append(None)

    def show_more_replies(self, comment):
        wd = comment.find_elements(by=By.CSS_SELECTOR, value="[aria-label='Show more replies']")
        if len(wd) != 0:
            self.driver.execute_script("arguments[0].click();", wd[0])
            print('clicked')
            # self.show_more_replies(comment)
        else:
            return

            # replies = mc.find_element_by_xpath('..//*[@id="replies"]')  # get the replies section of the above comment
            # if replies.text.startswith('View'):  # check if there are any replies
            #     replies.find_element_by_css_selector('a').click()  # if so open the replies
            #     time.sleep(3)  # wait for load (better strategy should be used here
            #     # replies = mc.find_elements(by=By.CLASS_NAME, value='ytd-comment-replies-renderer')
            # print(len(replies))
            # for reply in replies.find_elements_by_id('author-text'):
            #     print(reply.text)
            #     #reply_channel = reply.get_attribute('href')
            #     #print('Reply channel: ' + reply_channel)  # print the channel of each reply

    def accept_cookies(self):
        x = self.driver.find_element(by=By.CSS_SELECTOR,
                                     value="[aria-label='Accept the use of cookies and other data for the purposes described']")
        x.click()
        time.sleep(2)

    def skip_ad(self):
        button = self.driver.find_element(by=By.CLASS_NAME, value='ytp-ad-skip-button-container')
        button.click()

    def skip_trial(self):
        x = self.driver.find_element(by=By.CSS_SELECTOR, value="[aria-label='Skip trial']")
        x.click()

    def scroll_to_bottom(self):
        page_eng = False
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, 200)")  # initial sroll to load first comments
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


def main(line=None, sort_by=None):
    yt = YouTubeScraper('https://www.youtube.com/watch?v=Mb3tyjibXCg')
    yt.scrape()


if __name__ == '__main__':
    main()
