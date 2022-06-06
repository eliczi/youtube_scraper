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
df['likes'] = df['likes'].astype(str)
x = df['likes'].values
for i, v in enumerate(x):
    if v[-1] == 'K':
        x[i] = v[:-1] + '000'

df.loc[df['likes'][-1] == "K", "likes"] = df['likes'][:-1]
# Iterate over two given columns only from the dataframe
for column in df[['likes']]:
    # Select column contents by column name using [] operator
    columnSeriesObj = df[column]
    columnSeriesObj.values


class TextAnalysis:
    def __init__(self):
        self.df = pd.read_csv('df.csv', usecols=range(1, 6))

    def start(self):
        self.process_missing_data()
        self.copy_original_comment()
        
    def process_likes(self):
        self.df['likes'] = self.df['likes'].fillna(0)
        self.df.loc[self.df['likes'][-1] == "K", "likes"] = self.df['likes'][:-1]

        for row in self.df['likes']:
            if row[-1] == 'K':
                row = row[:-1]

            # self.df['likes'] =
            self.df['likes'] = self.df['likes'].fillna(0)

    def process_missing_data(self):
        self.df['comments'] = self.df['comments'].fillna('')

    def copy_original_comment(self):
        self.df['og_com'] = self.df['comments']

    def likes_to_number(self):
        self.df['likes'] = ''.join(self.df['likes'].split())

    # Top comments
    def top_comments(self, n=10):
        return self.df.sort_values(by='likes', ascending=False).head(n)

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


from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_font('arial', 'B', 12)
pdf.cell(60)
pdf.cell(75, 10, "A Tabular and Graphical Report of Professor Criss's Ratings by Users Charles and Mike", 0, 2, 'C')
pdf.output('test.pdf', 'F')
