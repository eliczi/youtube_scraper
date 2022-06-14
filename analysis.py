import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
import datetime
from scraper import YouTubeScraper
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import gensim.corpora as corpora
import gensim


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

    @staticmethod
    def convert_date(date):
        date = date.split()[:2]
        if 'week' in date[1]:
            date[1] = 'weeks'
        elif 'month' in date[1]:
            date[0] = int(date[0]) * 4
            date[1] = 'weeks'
        elif 'year' in date[1]:
            date[0] = int(date[0]) * 52
            date[1] = 'weeks'
        time_dict = {x: int(amount) for amount, x in [date]}
        dt = datetime.timedelta(**time_dict)
        return datetime.datetime.now() - dt

    # Top comments
    def top_comments(self, n=10):
        return self.df.sort_values(by='likes', ascending=False).head(n)

    def lower_case(self):
        self.df['comments'] = self.df['comments'].str.lower()

    def tokenize(self):
        for idx, row in self.df.iterrows():
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

    def stemming(self):
        ps = PorterStemmer()

        for idx, row in self.df.iterrows():
            self.df.at[idx, 'comments'] = [ps.stem(w) for w in self.df.at[idx, 'comments']]

    def top_words(self, n=10):
        self.join_words()
        most_common = Counter(" ".join(self.df["comments"]).split()).most_common(n)
        print('Most common words')
        for item in most_common:
            print(f"'{item[0]}':", item[1])
        print('\n')

    def most_liked_comments(self, n=10):
        print("Most liked comments:")
        most_liked = self.df.sort_values(by=['likes'], ascending=False).head(n)
        for idx, row in most_liked.iterrows():
            print(row['og_com'], '~', row['username'], f'- {row["likes"]} likes')

    def unique_word_comments(self, n):
        # number of comments in which given word appears
        my_dict = {}
        for comment in self.df['comments']:
            for word in comment:
                if word not in my_dict:
                    my_dict[f'{word}'] = 1
                elif comment.count(word) == 1:
                    my_dict[f'{word}'] += 1
        # Most popular words in unique comments
        most_common = Counter(my_dict).most_common(n)
        print('Most common unique comment words')
        for item in most_common:
            print(f"'{item[0]}':", item[1])
        print('\n')

    def ngrams(self, n, top_ngrams=10):
        all_words = []
        for comment in ta.df['comments'].values.tolist():
            all_words.extend(comment)
        n_grams = ngrams(all_words, n)
        ngram_counts = Counter(n_grams).most_common(top_ngrams)
        print(f'Top {top_ngrams} {n}-grams')
        for item in ngram_counts:
            print(item[0], item[1])

    def process(self):
        self.process_missing_data()
        self.likes_to_number()
        self.lower_case()
        self.tokenize()
        self.remove_stop_words()
        self.process_date()

    def analyse(self):
        self.process()
        self.top_words(15)
        self.tokenize()
        self.unique_word_comments(15)
        self.ngrams(2)
        self.most_liked_comments(10)
        self.lemmatizing()

    def topic(self, n):
        list_of_values = self.df['comments'].values.tolist()
        comments_dictionary = corpora.Dictionary(list_of_values)
        comments_dictionary.filter_extremes(no_above=0.9, no_below=ta.df['comments'].size * 0.05)
        corpus = [comments_dictionary.doc2bow(text) for text in list_of_values]

        lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                               id2word=comments_dictionary,
                                               num_topics=n)
        lda_model.print_topics()
        for idx, topic in lda_model.print_topics():
            print('Topic: {} \nWords: {}'.format(idx, topic))


ta = TextAnalysis()
ta.analyse()
ta.topic(3)
