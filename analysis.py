import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
df = pd.read_csv('data.csv')
df.columns = ['text']
df.insert(0, 'id', range(0, 0 + len(df)))
df['text'] = df['text'].astype(str).str.lower()
regexp = RegexpTokenizer('\w+')
df['text_token']=df['text'].apply(regexp.tokenize)

stopwords = nltk.corpus.stopwords.words("english")
my_stopwords = ['https']
stopwords.extend(my_stopwords)

df['text_token'] = df['text_token'].apply(lambda x: [item for item in x if item not in stopwords])


wordnet_lem = WordNetLemmatizer()

df['text_token'] = df['text_token'].apply(lambda x: [wordnet_lem.lemmatize(y) for y in x])


from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
df['stemmed'] = df['text_token'].apply(lambda x: [stemmer.stem(y) for y in x])

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


df['stemmed'] = df['stemmed'].apply(lambda x: ' '.join(x))
all_words = ' '.join([word for word in df['stemmed']])
words = nltk.word_tokenize(all_words)
fd = FreqDist(words)
fd.most_common()

import seaborn as sns
sns.set_theme(style="ticks")
top_10 = fd.most_common(100)
fdist = pd.Series(dict(top_10))

sns.barplot(y=fdist.index, x=fdist.values, color='blue')
