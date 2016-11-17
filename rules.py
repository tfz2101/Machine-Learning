import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
from util import get_data, plot_data

def getOrders(indicators, rule,*args,**kwargs):
    assert isinstance(indicators,pd.DataFrame), "Indicators have to be a dataframe with dates as index"



def ruleSTD(indicators,sigmas):
    orders = pd.DataFrame(index = indicators.index.values)
    for date in indicators.index.values:
        if indicators.ix[date,0] > 1:

test =  pd.DataFrame([[1,2,3]])
test2 = [1,2,3]
getOrders(test2)
