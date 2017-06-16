# Opistocks
This README explains the different aspects of the Opistocks project. The main programing language is Python3 (v3.6).

## Context and objectives of the project
This application aims at observing visually the correlation between a stock index on the trade markets and the public opinion on social media on the company.
The main objective is to be able to extract the most accurate opinion about a company based only on its stock index. Techniques of Machine Learning and Information Retrieval are used in this project. The analysis is performed on the last 7 days due to the Twitter API restriction.

## Data sets
There are two different kind of data ; namely the stock prices and the tweets. The stock prices are available through the [Yahoo Finance API](https://pypi.python.org/pypi/yahoo-finance/1.1.) that lets anyone have the price history of any company's index with a delay of 15 minutes on the real-time value.

The tweets are used in different ways and come from different sources. First, there are the annotated tweets used to train the classifiers to detect the sentiment of the text. The tweets come from [Crowdflower](https://www.crowdflower.com/data-for-everyone/). For our tests, we used 4 different data sets.

Name | # Tweets | Classes
----------------- | --------------- |------------------------------
[self-drive](https://www.crowdflower.com/wp-content/uploads/2016/03/Twitter-sentiment-self-drive-DFE.csv) | 7156 (213 Not Relevant) | [1, 5]
[text-emotion](https://www.crowdflower.com/wp-content/uploads/2016/07/text_emotion.csv) | 40000 (827 NR) | {sadness, enthusiasm, neutral, worry, surprise, love, fun, hate, happiness, boredom, relief, anger}
[apple](https://www.crowdflower.com/wp-content/uploads/2016/03/Airline-Sentiment-2-w-AA.csv) | 3886 (82 NR) | {1, 3, 5}
[airline](https://www.crowdflower.com/wp-content/uploads/2016/03/Apple-Twitter-Sentiment-DFE.csv) | 14641 | {negative, neutral, positive}

These tweets are then preprocessed following different strategies in order to find the model capable of extracting the sentiment out of a tweet. The different feature extraction strategies are the following :

- Tokenization: unigram VS bigram
- Stopwords: English list VS custom list
- Lowercase or Not
- Vector representation: Count (TF) VS TF-IDF

Each one the strategies are tested on every different machine learning algorithms tested in this project.

In addition of these data sets, the project also uses the [Twitter Search REST API](https://dev.twitter.com/overview/api) that allows developers to access a sample of published tweets in the last 7 days. These tweets are preprocessed with the same strategies used on previously mentioned tweets to train the classifier.

## Planning

- 28.04 - 5.05: Specification and feasibility study (All)
- 5.05 - 19.05: REST server implementation and "Stocks" routes integration (Fahy)
- 5.05 - 19.05: Web client skeleton implementation and "Stocks" visualization (Magnin)
- 5.05 - 2.06: Machine-Learning models evaluation (Höhn)
- 26.05 - 9.06: REST server integration of "Sentiment" + Best tags retrieval (Fahy)
- 26.05 - 9.06: Web client integration of "Sentiment" + Tests (Magnin)
- 9.06 - 16.06: Report and presentation (Höhn)

## Features and use cases
When the user arrives on the web application, he can only enter an index, and these actions are performed:

- 1) Download the stock price history on the last 7 days from Yahoo Finance API
- 2) Search 2 times for tweets on the Twitter API (one search on current day, another on day-7)
- 3) Extract the 5 most occurring tags in those ~200 tweets
- 4) Search 7 times for tweets (one search on every day)
- 5) Measure the sentiment mean value for each day based on the tweets and the Sentiment Analysis

## Technics, algorithms and tools used
The following sections describes for every major part of the project the technics, the tools and, if applicable, the algorithms.

### Machine-Learning
For Python, a popular and robust library is [scikit-learn](http://scikit-learn.org/stable/index.html). The visualization tool used in the model selection phase is [Jupyter notebook](http://jupyter.org).

Sentiment Analysis (SA) allows the computer to pull the sentiment from some information. The different sentiments range between a simple understanding (e.g. "Positive" or "Negative") to a more complex system which assigns a human sentiment such as "anger", "happiness", "sadness", or "love". As the sentiments, the information is found in multiple forms, like texts (from one sentence to a whole interview), images or speech.

In this project, the process of sentiment analysis is done following the machine learning approach. The different algorithms tested and evaluated are:

- Multinomial Naive Bayes (NB)
- SVM Linear Kernel
- SVM RBF Kernel

Support Vector Machine (SVM) is a type of statistical classifier where the data is separated by a hyperplane. During the training phase, the algorithm finds the optimal hyperplane that separates the two classes maximizing the margin between the hyperplane and the support vectors (i.e. closest vectors of the hyperplane). Different strategies exist to allow the SVM to work with multiple classes. "One-vs-rest" calculates a hyperplane that separates a class from the others and "One-vs-one" calculates a hyperplane for every couple of classes.

The Multinomial NB is a variant for text classification. Sklearn states that "the multinomial distribution normally requires integer feature counts. However, in practice, fractional counts such as tf-idf may also work.". This classifier is a probabilistic classifier that assigns for every input a probability to each class and the highest score determines the output class.

The parameters are kept default from the ones provided by sklearn.

- Multinomial NB: alpha (i.e. learning rate) = 1.0
- SVM Linear kernel: C (i.e. penalty parameter) = 1.0, multi-class = One-vs-rest
- SVM RBF kernel: C (i.e. penalty parameter) = 1.0, multi-class = One-vs-one

Due to some performance issues, the RBF kernel was not tested. The implementation works badly after 10k training elements and the computation time is quadratic.

The evaluation is done by training three models with 3 different data sets and test them with one data set.
The performance metric is the F1-Score which is the harmonic mean of the precision and the recall.

<img src="https://latex.codecogs.com/gif.latex?\text{F1-score}&space;=&space;\frac{2&space;\cdot&space;\text{precision}&space;\cdot&space;\text{recall}}{\text{precision}&space;&plus;&space;\text{recall}}" title="\text{F1-score} = \frac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}" />

The data sets are also equalized, meaning that the number of elements for each class is equal.

The best model is **Preprocessing strategy: custom stopwords + unigram tokenization + not lowercase, Training set: Airline, classifier: SVM Linear Kernel**

Class | precision | recall | f1-score | support
-------------- | -------------------- | ------------------- | ----------------- | ---------------------
negative | .70 | .48 | .57 | 423
neutral | .50 | .79 | .62 | 423
positive | .71 | .52 | .60 | 423
**avg / total** | **.64** | **.60** | **.60** | **1269**

The other results can be found in the [results visualization Jupyter notebook](https://github.com/rudolfhohn/Opistocks/blob/master/src/modelselection/results_visu.ipynb).

### Twitter Tags selection
The tools used for this part art [NLTK](http://nltk.org) and [Tweepy](http://tweepy.readthedocs.io).

The first step is to download two batches of tweets, one on the current day, and the other 7 days prior the current day. This two-step download aims at having the most probability of getting the most spoken tags. The query is done by:

- Filtering the retweets to avoid downloading multiple times the same tweet
- Using the index as the content of the query
- Using the results type query parameter to ask for "popular" tweets

Then, the tweets are preprocessed by (1) removing the stopwords, (2) lowercasing the text, (3) removes the punctuation, and (4) count the occurrences. On this basis, **5** most used tags are extracted.

The next search queries are constructed following certain rules and choices.

- The content of the query are the tags and the index with the "OR" operator, meaning that Twitter will send us tweets that contain at least one of the tokens
- The sentiment is measured by day, therefore one search is thrown by day
- The retweets are also filtered
- Type of results is set as "mixed", instead of "popular", to have a wider range of opinions

### Stock market history price
The tools used for this part are [Yahoo Finance API](https://pypi.python.org/pypi/yahoo-finance/1.1.) and [Pandas](http://pandas.pydata.org).

Before trying downloading the stock market history, the server tests is the index exists. Then, the history is downloaded on the 7 past days. Because the market is closed on weekends and during holidays, the range of available days are between 5 and 7. The results are kept and manipulated using *DataFrames*.

On 25th May, Yahoo Finance stopped their API support and closed the main address. However, we were able to find another way of calling the API (secondary route) but we do not know for how long it will still be available.

### Web client
The web client is developed using mainly JavaScript libraries, with the [AngularJS framework](http://angularjs.org). The libraries are [Bootstrap](http://getbootstrap.com), [Moment.js](http://momentjs.com) and [Chart.js](http://www.chartjs.org).

When the user enters an index, the server checks if the index exists. If it does, the stock and opinions values are retrieved for 7 days. The Chart is displayed with two different *y* axis, one for the stock price and the other for the sentiment value that ranges between 1 and 5, being respectively the most negative and most positive sentiment.

## Conclusion
The project is finished, the specifications are fulfilled. However, the limitations due to the Twitter API are very constraining. The project would be more interesting and with a potential real use if Twitter would let developers access all their tweets.
