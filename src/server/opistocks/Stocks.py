# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from flask import jsonify
import json
import pandas as pd
from pandas_datareader import data, wb
from yahoo_finance import Share


class Stocks:
    """Stocks class

    Using the yahoo_finance API and pandas to :

        - retrieve historical data (pandas, because its faster)
        - check if an index exists (yahoo_finance)
    """
    instance = None

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
                df = data.DataReader(self.index, 'yahoo', datetime(1900, 1, 1),
                                     datetime.today())['Adj Close']
                # Convert the date format from timestamp to YYYYMMDD
                dates = [int(pd.to_datetime(x).strftime("%Y%m%d")) for x in df.index.values.tolist()]
                self._data = [list(a) for a in zip(dates,
                              df.values.tolist())]
            return self._data

        def get_all_hist(self):
            """Get historical data of index."""
            return json.dumps(self.data)

        def get_hist_between_dates(self, date_start, date_end):
            """Get historical data of index between dates."""
            try:
                if self.is_index():
                    # Change format of dates
                    d_start = datetime.strptime(date_start, '%Y%m%d')
                    d_end = datetime.strptime(date_end, '%Y%m%d')
                    # Retrieve the data
                    df = data.DataReader(self.index, 'yahoo', d_start, d_end)['Adj Close']
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

