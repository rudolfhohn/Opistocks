import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV, train_test_split

# self-drive
df_sd = pd.read_csv('../data/Twitter-sentiment-self-drive-DFE.csv', encoding='latin1')

# remove not relevant tweets
df_sd = df_sd[~df_sd['sentiment'].isin(['not_relevant'])]

# create the main dataframe by extracting the relevant rows
df = pd.concat([df_sd['text'], df_sd['sentiment']], axis=1, keys=['text', 'sentiment'])

# normalize the sentiment values ({1; 2; 3; 4; 5} => {-1; 0; 1})
df['sentiment'] = df['sentiment'].map({'1':-1, '2':-1, '3':0, '4':1, '5':1})
del df_sd

# text-emotion
df_te = pd.read_csv('../data/text_emotion.csv')
df_te = pd.concat([df_te['content'], df_te['sentiment']], axis=1, keys=['text', 'sentiment'])

# remove not relevant tweets
df_te = df_te[~df_te['sentiment'].isin(['empty'])]

# map words into integer values ({...} => {-1; 0; 1})
df_te['sentiment'] = df_te['sentiment'].map({
    'sadness':-1,
    'enthusiasm':1,
    'neutral':0,
    'worry':-1,
    'surprise':1,
    'love':1,
    'fun':1,
    'hate':-1,
    'happiness':1,
    'boredom':-1,
    'relief':1,
    'anger':-1})

# append the rows to the main dataframe
df = df.append(df_te)
del df_te

# apple
df_ap = pd.read_csv('../data/Apple-Twitter-Sentiment-DFE.csv', encoding='latin1')
df_ap = pd.concat([df_ap['text'], df_ap['sentiment']], axis=1, keys=['text', 'sentiment'])

# remove not relevant tweets
df_ap = df_ap[~df_ap['sentiment'].isin(['not_relevant'])]

# normalize the sentiment values ({1; 3; 5} => {-1; 0; 1})
df_ap['sentiment'] = df_ap['sentiment'].map({'1':-1, '3':0, '5':1})

# append the rows to the main dataframe
df = df.append(df_ap)
del df_ap

# airline
df_ai = pd.read_csv('../data/Airline-Sentiment-2-w-AA.csv', encoding='latin1')
df_ai = pd.concat([df_ai['text'], df_ai['airline_sentiment']], axis=1, keys=['text', 'sentiment'])

# normalize the sentiment values ({'negative'; 'neutral'; 'positive'} => {-1; 0; 1})
df_ai['sentiment'] = df_ai['sentiment'].map({'negative':-1, 'neutral':0, 'positive':1})

# append the rows to the main dataframe
df = df.append(df_ai)
del df_ai

# Array of vectorizers for the feature extraction step
vecs = [
    CountVectorizer(stop_words='english', ngram_range=(1, 1), lowercase=True),
    CountVectorizer(stop_words='english', ngram_range=(1, 1), lowercase=False),
    CountVectorizer(stop_words='english', ngram_range=(2, 2), lowercase=True),
    CountVectorizer(stop_words='english', ngram_range=(2, 2), lowercase=False),
    CountVectorizer(stop_words=None, ngram_range=(1, 1), lowercase=True),
    CountVectorizer(stop_words=None, ngram_range=(1, 1), lowercase=False),
    CountVectorizer(stop_words=None, ngram_range=(2, 2), lowercase=True),
    CountVectorizer(stop_words=None, ngram_range=(2, 2), lowercase=False),
    TfidfVectorizer(stop_words='english', ngram_range=(1, 1), lowercase=True),
    TfidfVectorizer(stop_words='english', ngram_range=(1, 1), lowercase=False),
    TfidfVectorizer(stop_words='english', ngram_range=(2, 2), lowercase=True),
    TfidfVectorizer(stop_words='english', ngram_range=(2, 2), lowercase=False),
    TfidfVectorizer(stop_words=None, ngram_range=(1, 1), lowercase=True),
    TfidfVectorizer(stop_words=None, ngram_range=(1, 1), lowercase=False),
    TfidfVectorizer(stop_words=None, ngram_range=(2, 2), lowercase=True),
    TfidfVectorizer(stop_words=None, ngram_range=(2, 2), lowercase=False)
]

def feat(df, vec):
    return vec.fit_transform(df['text'].as_matrix()).toarray(), df['sentiment'].as_matrix()


SEED = 17
results = []

df = df.sample(n=1000)


for idx, vec in enumerate(vecs):
    current_vec = vec
    X, y = current_vec.fit_transform(df['text'].as_matrix()).toarray(), df['sentiment'].as_matrix()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=SEED)


print(X_train)
