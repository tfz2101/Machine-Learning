import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
#from pykalman import KalmanFilter
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf,pacf, adfuller
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from operator import itemgetter
from sklearn import linear_model as LM


DATA_PATH = "L:\Trade_Data.xlsx"
TAB_NAME = "Data"
SIGNAL_COL = "STD of Move"
ENTRY_COL ="IsEntry"
HIT_COL ="Hit Ratio for 1 HP"
DIRECTION_COL = "Direction"
CHANGE_COL = "Change"
PNL_COL = "Pnl"




def getEntrySD(sd, trigger):
    if abs(sd) > trigger:
        return "TRADE"
    else:
        return np.nan

def getHitOrNot(direction,change):
    #print(type(direction))
    assert isinstance(direction,np.float64), "Direction needs to be an integer"
    if direction * change > 0:
        return 1
    else:
        return 0

def getTradeDirection(signal):
    return (signal/abs(signal) * -1)

def getPnl(direction,change):
    assert isinstance(direction,np.float64), "Direction needs to be an integer"
    return (direction * change)

#Calc PnL Columns
'''
#Calc Trade or Not column
threshold = 1.5
for a in data.index.values:
    data.ix[a,ENTRY_COL] = getEntrySD(data.ix[a,SIGNAL_COL],threshold)

#Calc Trade Direction
for a in data.index.values:
    if data.loc[a,ENTRY_COL]=="TRADE":
        data.loc[a,DIRECTION_COL] = getTradeDirection(data.loc[a,SIGNAL_COL])

#Calc Hit or Not
for i in range(1,data.shape[0]):
    if data.loc[a,ENTRY_COL]=="TRADE":
        data.ix[i,HIT_COL]=getHitOrNot(data.ix[i,DIRECTION_COL],data.ix[i-1,CHANGE_COL])

#Calc PnL
for i in range(1,data.shape[0]):
    if data.loc[a,ENTRY_COL]=="TRADE":
        data.ix[i,PNL_COL]=getPnl(data.ix[i,DIRECTION_COL],data.ix[i-1,CHANGE_COL])
'''