import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import datetime
from scraper import YouTubeScraper
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams


# ys = YouTubeScraper('https://www.youtube.com/watch?v=54kz9zv_080')
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
        self.copy_original_comment()

    def start(self):
        self.process_missing_data()
        self.copy_original_comment()

    def process_missing_data(self):
        self.df = self.df[self.df['comments'].notna()]
        self.df['likes'] = self.df['likes'].fillna(0)

    def copy_original_comment(self):
        self.df['og_com'] = self.df['comments']

    def likes_to_number(self):
        for i, row in self.df.iterrows():
            if 'K' in str(row['likes']):
                if '.' in str(row['likes']):
                    row['likes'] = str(row['likes']).replace('.', '').replace('K', '00')
                else:
                    row['likes'] = str(row['likes']).replace('K', '00')
        self.df['likes'] = self.df['likes'].astype(int)

    def process_date(self):
        self.df['date'] = self.df['date'].apply(self.convert_date)

    def convert_date(self, date):
        date = date.split()[:2]
        if 'month' in date[1]:
            date[0] = int(date[0]) * 4
        elif 'year' in date[1]:
            date[0] = int(date[0]) * 52
        date[1] = 'weeks'
        time_dict = dict((fmt, float(amount)) for amount, fmt in [date])
        dt = datetime.timedelta(**time_dict)
        return datetime.datetime.now() - dt

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

    def join_words(self):
        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = str(' '.join(self.df.at[idx, 'comments']))

    def remove_stop_words(self):
        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '?', '``', "''", "'", "'s", "!", "’", "would", "n't", '“', '”', ":"])
        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = [w for w in self.df.at[idx, 'comments'] if not w in stop_words]

    def lemmatizing(self):
        lemmatizer = WordNetLemmatizer()
        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = [lemmatizer.lemmatize(w) for w in self.df.at[idx, 'comments']]

        pass

    def stemming(self):
        ps = PorterStemmer()

        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = [ps.stem(w) for w in self.df.at[idx, 'comments']]

    def top_words(self, n=10):
        self.join_words()
        return Counter(" ".join(self.df["comments"]).split()).most_common(n)
        self.tokenize()

    def most_liked_comments(self, n=10):
        return self.df.sort_values(by=['likes'], ascending=False).head(n)

    def i_dont_know_how_to_call_this_function(self):
        # number of comments in which given word appears
        my_dict = {}
        for comment in ta.df['comments']:
            for word in comment:
                if word not in my_dict:
                    my_dict[f'{word}'] = 1
                elif comment.count(word) == 1:
                    my_dict[f'{word}'] += 1
        # for w in sorted(my_dict, key=my_dict.get, reverse=True):
        #     print(w, my_dict[w])

    def ngrams(self, n, top_ngrams=10):
        all_words = []
        for comment in ta.df['comments'].values.tolist():
            all_words.extend(comment)
        n_grams = ngrams(all_words, n)
        ngram_counts = Counter(n_grams)
        ngram_counts.most_common(top_ngrams)

    def process(self):
        self.process_missing_data()
        self.likes_to_number()
        self.lower_case()
        self.tokenize()
        self.remove_stop_words()
        self.process_date()

    def analyse(self):
        ta.top_words(15)
        most_liked = self.most_liked_comments(10)
        self.lemmatizing()

        
ta = TextAnalysis()
ta.process_date()

from collections import Counter

# n grams


dupa = ta.df['comments'].values.tolist()
ta.df = ta.df.loc[ta.df['comments'] != '']
import gensim.corpora as corpora
import gensim

lst = ta.df['comments'].values.tolist()

com_dict = corpora.Dictionary(lst)
com_dict.filter_extremes(no_above=0.9, no_below=ta.df['comments'].size * 0.05)
texts = lst
corpus = [com_dict.doc2bow(text) for text in texts]

lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=com_dict,
                                       num_topics=5)
lda_model.print_topics()
print(lda_model.print_topics())
doc_lda = lda_model[corpus]

from gensim import corpora, models

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break
lda_model = gensim.models.LdaMulticore(corpus, num_topics=10, id2word=com_dict, passes=2, workers=2)
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=com_dict, passes=2, workers=4)
for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))
