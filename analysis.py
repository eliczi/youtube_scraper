from scraper import YouTubeScraper
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter


# ys = YouTubeScraper('https://www.youtube.com/watch?v=zxaXgNJG3xk')
# ys.scrape()
# data = ys.comments
# replies = ys.comments['replies']  # list of dictionaries, 10th comment replies is 10th list element as a dict
# data.pop('replies', None)
# df = pd.DataFrame(data)
# df.to_csv('df.csv')
# # read without first column


class TextAnalysis:
    def __init__(self):
        self.df = pd.read_csv('df.csv', usecols=range(1, 6))

    def start(self):
        self.process_missing_data()
        self.copy_original_comment()

    def process_missing_data(self):
        self.df['comments'] = self.df['comments'].fillna('')
        self.df['likes'] = self.df['likes'].fillna(0)

    def copy_original_comment(self):
        self.df['og_com'] = self.df['comments']

    def likes_to_number(self):
        self.df['likes'] = self.df['likes'].replace('K', '000', regex=True)

    def process_date(self):
        # use timedelta
        pass

    # Top comments
    def top_comments(self, n=10):
        return self.df.sort_values(by='likes', ascending=False).head(n)

    def lower_case(self):
        self.df['comments'] = self.df['comments'].str.lower()

    def tokenize(self):
        # tokenize and lower case
        for idx, row in self.df.iterrows():  # tokenize and lower case
            if self.df.at[idx, 'comments'] != '':
                self.df.at[idx, 'comments'] = word_tokenize(self.df.at[idx, 'comments'])
                for i, word in enumerate(self.df.at[idx, 'comments']):
                    self.df.at[idx, 'comments'][i] = word.lower()

    def join_words(self):
        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = str(' '.join(self.df.at[idx, 'comments']))

    def remove_stop_words(self):
        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '?', '``', "''", "'", "'s", "!", "’"])
        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = [w for w in self.df.at[idx, 'comments'] if not w in stop_words]

    def stemming(self):
        ps = PorterStemmer()

        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = [ps.stem(w) for w in self.df.at[idx, 'comments']]

    def top_words(self, n):
        self.join_words()
        Counter(" ".join(self.df["comments"]).split()).most_common(n)


ta = TextAnalysis()
ta.process_missing_data()
ta.likes_to_number()
ta.lower_case()

import datetime

s = "3 months ago"
parsed_s = [s.split()[:2]]
time_dict = dict((fmt, float(amount)) for amount, fmt in parsed_s)

dt = datetime.timedelta(**time_dict)
past_time = datetime.datetime.now() - dt
print(past_time)
