'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : 

@Date          : Nov 2021

Technical Indicators

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

from datetime import date
from scipy.stats import norm

from math import log, exp, sqrt

from stock import *


class SimpleMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''

    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._sma = {}

    def _calc(self, period, price_source):
        '''
        for a given period, calc the SMA as a pandas series from the price_source
        which can be  open, high, low or close
        '''
        result = None
        # TODO
        # df_ohlcv_price_source = self.ohlcv_df[price_source]
        # df_ohlcv_price_source_rolling = df_ohlcv_price_source.rolling(
        #     period, min_periods=1)
        # result = df_ohlcv_price_source.mean()
        result = self.ohlcv_df[price_source].rolling(
            period, min_periods=1).mean()
        # end TODO
        return(result)

    def run(self, price_source='close'):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._sma[period] = self._calc(period, price_source)

    def get_series(self, period):
        return(self._sma[period])


class ExponentialMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''

    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._ema = {}

    def _calc(self, period):
        '''
        for a given period, calc the SMA as a pandas series
        '''
        result = None
        # TODO: implement details here
        # ewm() -> a function to calculate the exponentially weighted moving average
        # for a certain number of previous periods in Pandas
        # df_ohlcv_price_source = self.ohlcv_df
        # df_ohlcv_price_source_close_ewm = df_ohlcv_price_source['close'].ewm(
        #     span=period, adjust=False)
        # result = df_ohlcv_price_source_close_ewm.mean()
        result = self.ohlcv_df['close'].ewm(span=period, adjust=False).mean()
        # end TODO
        return(result)

    def run(self):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._ema[period] = self._calc(period)

    def get_series(self, period):
        return(self._ema[period])


class RSI(object):

    def __init__(self, ohlcv_df, period=14):
        self.ohlcv_df = ohlcv_df
        self.period = period
        self.rsi = None

    def get_series(self):
        return(self.rsi)

    def run(self):
        '''
        calculate RSI
        0. RSI = 100 - 100/(1+RS)
        1. RS = AVG Gain / AVG Loss
        2. N = 14
        3. AVG Gain = 1/14 * Current Gain + 13/14 * Previous Average Gain
        4. AVG Loss = 1/14 * Current Loss + 13/14 * Previous Average Loss
        '''
        # diff = self.ohlcv_df['close'].diff()

        # gain = diff.copy()
        # gain[diff <= 0] = 0.0

        # loss = abs(diff.copy())
        # loss[diff > 0] = 0.0

        # avg_gain = gain.ewm(com=13, adjust=False, min_periods=14).mean()
        # avg_loss = loss.ewm(com=13, adjust=False, min_periods=14).mean()

        # try:
        #     rs = abs(avg_gain/avg_loss)
        #     self.rsi = 100-100/(1+rs)
        # except ZeroDivisionError:
        #     print("Can not divide by zero")
        # # end TODO

        # return(self.rsi)
        # TODO: implement details here
        current_different = self.ohlcv_df['close'].diff()
        current_gain = current_different.copy()
        current_gain[current_different <= 0] = 0  # loss = 0

        current_loss = current_different.copy()
        current_loss[current_different > 0] = 0  # gain = 0
        current_loss = abs(current_loss)

        gain_mean = current_gain.ewm(
            com=13, adjust=False, min_periods=14).mean()
        loss_mean = current_loss.ewm(
            com=13, adjust=False, min_periods=14).mean()

        rs = abs(gain_mean/loss_mean)
        self.rsi = 100-100/(1+rs)
        # RSI -> 1. RS = Avg Gain / AVG Loss
        return self.rsi
        # end TODO


class VWAP(object):

    def __init__(self, ohlcv_df):
        self.ohlcv_df = ohlcv_df
        self.vwap = None

    def get_series(self):
        return(self.vwap)

    def run(self):
        '''
        calculate VWAP
        '''
        price = (self.ohlcv_df['high'] +
                 self.ohlcv_df['low'] + self.ohlcv_df['close']) / 3
        self.vwap = (
            (self.ohlcv_df['volume'] * price).cumsum()) / self.ohlcv_df['volume'].cumsum()
        return self.vwap
        # TODO: implement details here
        # end TODO


def _test():
    # simple test cases
    symbol = 'AAPL'
    stock = Stock(symbol)
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    stock.get_daily_hist_price(start_date, end_date)

    periods = [9, 20, 50, 100, 200]
    smas = SimpleMovingAverages(stock.ohlcv_df, periods)
    smas.run()
    s1 = smas.get_series(9)
    print(s1.index)
    print(s1)

    rsi_indicator = RSI(stock.ohlcv_df)
    rsi_indicator.run()

    print(f"RSI for {symbol} is {rsi_indicator.rsi}")


if __name__ == "__main__":
    _test()
