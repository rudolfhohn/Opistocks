# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import sklearn
import pandas as pd
import pickle

from instance import config

import tweepy
from dateutil.parser import parse
from itertools import chain
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
from collections import Counter
import numpy as np

class Sentiment:
    """Sentiment class

    Interface to a SVM (Linear kernel) and its Vectorizer to classifiy into
    3 classes (positive, neutral, negative) tweets.
    """
    instance = None

    def __init__(self):
        if not Sentiment.instance:
            Sentiment.instance = Sentiment.__Sentiment()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Sentiment:
        """Singleton class"""
        PICKLE_FILE = 'opistocks_classifier_vectorizer_prod.pickle'

        def __init__(self):
            """Init of class

            Load the classifier and the vectorizer
            """
            self.classifier, self.vectorizer = pickle.load(open(self.PICKLE_FILE, 'rb'))

        def sentiment(self, tweet):
            vec = self.vectorizer.transform([tweet])
            return int(str(self.classifier.predict(vec)[0]))

        def get_sentiments_twitter(self, index):
            date_end = datetime.today().strftime('%Y%m%d')
            date_start = str(int(date_end) - 7)
            return self.get_sentiments_twitter_between_dates(index, date_start, date_end)

        def get_sentiments_twitter_between_dates(self, index, date_start, date_end):
            """Sentiment value from tweets over a period of time

            This method works in different steps.
            1)  Search two times for tweets distributed over the period selected
                for the wanted stock market index
            2)  Determine the N most used tags in the previously downloaded tweets
            3)  Search one time per day the tweets with the N most used tags
            4)  Format the retrieved tweets to send them in response of the API call
            """
            N_TAGS = 5
            SEND_TWEETS = False

            # Change format of dates
            d_start = parse(date_start).strftime('%Y-%m-%d')
            d_end = parse(date_end).strftime('%Y-%m-%d')

            # Authentify to Twitter API
            consumer_key = config.CONSUMER_KEY
            consumer_secret = config.CONSUMER_SECRET
            access_token = config.ACCESS_TOKEN
            access_token_secret = config.ACCESS_TOKEN_SECRET

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)

            # Search tweets
            query = '{} -filter:retweets'.format(index)
            results_search_end = api.search(q=query, lang='eng', results_type='popular', count=100, until=d_end)
            results_search_start = api.search(q=query, lang='eng', results_type='popular', count=100, until=d_start)
            results = [{'text': x._json['text'], 'created_at': x._json['created_at']} for x in list(chain(results_search_start, results_search_end))]

            # N most used tags
            tokenizer = TweetTokenizer()
            l = list(chain.from_iterable([tokenizer.tokenize(tweet['text']) for tweet in results]))
            stop = set(stopwords.words('english'))
            l = [i.lower() for i in l if i.lower() not in stop]
            l = [i for i in l if i not in string.punctuation]
            tags = [i[0] for i in Counter(l).most_common(N_TAGS)]

            # Retrieve sentiments for tweets
            tweets = []
            for i in range(int(date_end) - int(date_start) + 1):
                cur_date = parse(str(int(date_start) + i)).strftime('%Y-%m-%d')
                query = '{} OR {} -filter:retweets'.format(index, ' OR '.join(tags))
                tweets.append(api.search(q=query, lang='eng', results_type='mixed', count=100, until=cur_date))

            # Analyze tweets
            tweets = [{'text': x._json['text'],
                    'created_at': parse(x._json['created_at']).strftime('%Y%m%d'),
                    'sentiment': self.sentiment(x._json['text'])} for x in list(chain.from_iterable(tweets))]

            # Separate the tweets by date
            tweets_date = {}
            for t in tweets:
                cur_date = int(t['created_at'])
                if cur_date not in tweets_date.keys():
                    tweets_date[cur_date] = [[], []]
                tweets_date[cur_date][0].append(t['text'])
                tweets_date[cur_date][1].append(t['sentiment'])

            # Mean sentiment by date
            data = []
            for key, value in tweets_date.items():
                mean_sentiment = np.mean(value[1])
                if SEND_TWEETS:
                    data.append([key, mean_sentiment, list(zip(value[0], value[1]))])
                else:
                    data.append([key, mean_sentiment])

            return data
