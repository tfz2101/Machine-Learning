

import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
from util import get_data, plot_data

def getOrders(indicators, rule,**kwargs):
    assert isinstance(indicators,pd.DataFrame), "Indicators have to be a dataframe with dates as index"
    return rule(indicators,**kwargs)


def ruleSTD(indicators,sigmas):
    print(indicators)
    orders = []
    for i in range(0,indicators.shape[0]):
        if indicators.iloc[i,0] >= sigmas:
           orders.append([indicators.index.values[i],'IBM','SELL',1])
        if indicators.iloc[i,0] <= -sigmas:
           orders.append([indicators.index.values[i],'IBM','BUY',1])
    print('orders list version',orders)
    orders = pd.DataFrame(orders,columns = ['Date','Symbol','Order','Shares'])
    return orders
test =  pd.DataFrame([[1,2,3]])
test2 = [1,2,3]

#getOrders(test2)
