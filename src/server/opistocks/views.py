# -*- coding: utf-8 -*-

from opistocks import app
from .Stocks import Stocks
from .Sentiment import Sentiment
import json
import numpy as np

from flask import jsonify, Response


@app.route('/stocks/<index>')
def get_stocks(index):
    """
    @api {get} /stocks/<index> Request all stocks values from <index>
    @apiName get_stocks
    @apiGroup stocks
    @apiDescription Get all historic values for stocks.
    The value is the adjusted closing price of the day.

    @apiParam {index} index     Intex to request the historic from

    @apiSuccess {String} date   Date related to the value
    @apiSuccess {String} value  Adjusted closing price of the stock for the related date

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "date": "20160112",
            "value": "15.04"
        },
        {
            "date": "20160113",
            "value": "19.04"
        }
    """
    stock = Stocks(index)
    return Response(json.dumps(stock.data), mimetype='application/json')


@app.route('/stocks/<index>/<date_start>/<date_end>')
def get_stocks_between_date(index, date_start, date_end):
    """
    @api {get} /stocks/:index/:date_start/:date_end Request stocks values of <index> between <date_start> and <date_end>
    @apiName get_stocks_between_date
    @apiGroup stocks
    @apiDescription Get all historic values for stocks.
    The value is the adjusted closing price of the day.

    @apiParam {index} index         Index to request the historic from
    @apiParam {String} date_start   Start date for the historic
    @apiParam {String} date_end     End date for the historic

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "date": "20160112",
            "value": "15.04"
        },
        {
            "date": "20160113",
            "value": "19.04"
        }
    """
    stock = Stocks(index)
    return Response(json.dumps(stock.get_hist_between_dates(date_start, date_end)), mimetype='application/json')


# Route to check if an index exists
@app.route('/index/<index>')
def check_index(index):
    """
    @api {get} /index/:index Check if index exists
    @apiName check_index
    @apiGroup index
    @apiDescription Check wheter an index exists.

    @apiParam {String} index Index to check the existence.

    @apiSuccess {Boolean} valid  Return true if index exists, else false

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "valid": true,
        }
    """
    stock = Stocks(index)
    if stock.is_index():
        return jsonify(valid=True)
    else:
        return jsonify(valid=False)


# Route to predict the sentiment value of a tweet
@app.route('/sentiment/<tweet>')
def sentiment(tweet):
    """
    @api {get} /sentiment/:tweet Predict sentiment of tweet
    @apiName sentiment
    @apiGroup sentiment
    @apiDescription Predict the sentiment of a tweet with a classifier (SVM)

    @apiParam {String} tweet Tweet to classify

    @apiSuccess {Integer} sentiment  Return 1 for negative, 3 neutral, 5 positive

    @apiSuccessExample Success-Response:
        HTTP/1.1 200 OK
        {
            "sentiment": 5
        }
    """
    s = Sentiment()
    sent = s.sentiment(tweet)
    return jsonify(sentiment=np.asscalar(np.int16(sent)))

@app.route('/sentiment/<index>/<date_start>/<date_end>')
def get_sentiment_between_date(index, date_start, date_end):
    """
    @api {get} /sentiment/:index/:date_start/:date_end Request sentiment values of <index> between <date_start> and <date_end>
    @apiName get_sentiment_between_date
    @apiGroup sentiment
    @apiDescription Get all sentiment values between two days on Twitter

    @apiParam {index} index         Index to request the historic from
    @apiParam {String} date_start   Start date for the historic
    @apiParam {String} date_end     End date for the historic
    """
    s = Sentiment(index)
    return Response(json.dumps(s.get_sentiments_twitter_between_dates(date_start, date_end)), mimetype='application/json')
