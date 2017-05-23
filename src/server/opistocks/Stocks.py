# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from flask import jsonify
import json
import pandas as pd
from pandas_datareader import data, wb
from yahoo_finance import Share
import requests
import os
import yaml
import re
import io


class Stocks:
    """Stocks class

    Using the yahoo_finance API and pandas to :

        - retrieve historical data (pandas, because its faster)
        - check if an index exists (yahoo_finance)

    WARNING: since the 18th May 2017, the API from Yahoo as been terminated.
    This method to retrieve financial data is a big hack and will probably not last.
    This trick is based on: https://github.com/sjev/trading-with-python/blob/master/scratch/get_yahoo_data.ipynb
    """
    instance = None
    # Url for yahoo, stock needs to be inserted between START_URL and END_URL
    START_URL = 'https://uk.finance.yahoo.com/quote/'
    END_URL = '/history'

    def __init__(self, index):
        if not Stocks.instance:
            Stocks.instance = Stocks.__Stocks(index)
        else:
            Stocks.instance.index = index
            Stocks.instance.stock = Share(index)
            Stocks.instance._data = None

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __Stocks:
        """Singleton class"""

        def __init__(self, index):
            """Init of class

            Load the index.
            """
            self.index = index
            self.stock = Share(index)
            self._data = None

        @property
        def data(self):
            """Getter of data.
            If data are not loaded, load them.
            """
            if self._data is None:
                print('Loading data of {}'.format(self.index))
                self.get_hist_between_dates('19000101', datetime.today().strftime('%Y%m%d'))
            return self._data

        def get_all_hist(self):
            """Get historical data of index."""
            return json.dumps(self.data)

        def get_hist_between_dates(self, date_start, date_end):
            """Get historical data of index between dates."""
            try:
                if self.is_index():
                    # Creation of the url
                    url = Stocks.START_URL + self.index + Stocks.END_URL
                    # Download the page
                    r = requests.get(url)
                    txt = r.text
                    cookie = r.cookies['B'] # the cooke we're looking for is named 'B'
                    print('Cookie: ', cookie)

                    # Now we need to extract the token from html.
                    # the string we need looks like this: "CrumbStore":{"crumb":"lQHxbbYOBCq"}
                    # regular expressions will do the trick!
                    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

                    for line in txt.splitlines():
                        m = pattern.match(line)
                        if m is not None:
                            crumb = m.groupdict()['crumb']

                    print('Crumb=',crumb)

                    # Create data directory in the user folder
                    dataDir = os.getcwd() + '/twpData'

                    if not os.path.exists(dataDir):
                        os.mkdir(dataDir)

                    # Save data to YAML file
                    data = {'cookie':cookie,'crumb':crumb}

                    dataFile = os.path.join(dataDir,'yahoo_cookie.yml')

                    with open(dataFile,'w') as fid:
                        yaml.dump(data,fid)

                    # Change format of dates
                    d_start = datetime.strptime(date_start, '%Y%m%d').timestamp()
                    d_end = datetime.strptime(date_end, '%Y%m%d').timestamp()

                    # Prepare input data as a tuple
                    data = (int(d_start),
                            int(d_end),
                            crumb)

                    url = "https://query1.finance.yahoo.com/v7/finance/download/VXX?period1={0}&period2={1}&interval=1d&events=history&crumb={2}".format(*data)

                    print(url)
                    # Retrieve the data
                    data = requests.get(url, cookies={'B':cookie})

                    buf = io.StringIO(data.text) # Create a buffer
                    df = pd.read_csv(buf,index_col=0)['Adj Close'] # Convert to pandas DataFrame

                    # Convert the date format from timestamp to YYYYMMDD
                    dates = [int(pd.to_datetime(x).strftime("%Y%m%d")) for x in df.index.values.tolist()]
                    self._data = [list(a) for a in zip(dates,
                                  df.values.tolist())]
                    return self._data
            except Exception as e:
                print('Error while getting historic of data : {}'.format(e))
                return None

        def is_index(self):
            """Check if an index exists."""
            try:
                return bool(self.stock.get_name())
            except:
                return False

        def get_name(self):
            """Get the name of the index."""
            return self.stock.get_name()

