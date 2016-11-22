
import pandas as pd
import numpy as np
import datetime as dt
import time as time
from util import get_data, plot_data


start_date = dt.datetime(2008,1,1)
end_date = dt.datetime(2012,1,1)
datesIndex = pd.date_range(start_date,end_date,freq='1D').tolist()
symbols = ['IBM']
IBM_Data = get_data(symbols,datesIndex,addSPY=False)
IBM_Data= IBM_Data.dropna()

def getMACDValues(data,slowFreq, fastFreq, stdFreq):
    slow_MA = pd.rolling_mean(data,slowFreq)
    fast_MA = pd.rolling_mean(data,fastFreq)
    diff = fast_MA - slow_MA
    diff_std = pd.rolling_std(arg=diff,window=stdFreq)

    #print(diff_std)
    MACD = diff/diff_std
    #print(MACD)
    return MACD

def getRSIValues(data,freq):
    diffs = data.diff(1)
    def RSI(data):
        #print('raw row',data)
        avg_up = data[data>=0].mean()
        #print('avg up',avg_up)
        avg_down = abs(data[data<0].mean())
        #print("avg_down",avg_down)

        rsi = avg_up/avg_down
        if avg_up/avg_up != 1: rsi = 0
        elif avg_down/avg_down != 1: rsi = 99
        #print('rsi',rsi)
        return 100-100/(1+rsi)

    out = pd.rolling_apply(arg=diffs,window=freq,func=RSI,min_periods=freq)
    #print(data)
    #print(out)
    return out



#getMACDValues(IBM_Data,10,3,5)
getRSIValues(IBM_Data,10)
