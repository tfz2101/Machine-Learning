import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
from util import get_data, plot_data

def getOrders(indicators, rule,**kwargs):
    assert isinstance(indicators,pd.DataFrame), "Indicators have to be a dataframe with dates as index"
    return rule(indicators,**kwargs)


class tradingRules(object):

    def __init__(self,holdingPer = 10,maxHoldings=500):
        self.position = 0
        self.lastEntryDate = 0
        self.holdingPer = holdingPer
        self.maxHoldings =  maxHoldings
        self.unit = 500


    def ruleSTD(self,indicators,thresh0_High,thresh0_Low,thresh1_High,thresh1_Low,thresh2_High,thresh2_Low):
        orders = []
        self.position = 0
        self.lastEntryDate = dt.datetime(1800,1,1)
        for i in range(0,indicators.shape[0]):
            tempPos = self.position
            if (indicators.iloc[i,0] >= thresh0_High) and (indicators.iloc[i,1] >= thresh1_High) and (indicators.iloc[i,2] >= thresh2_High):
               temp = [indicators.index.values[i],'IBM','BUY',self.unit]
               tempPos =+ self.unit
            if (indicators.iloc[i,0] < thresh0_Low) and (indicators.iloc[i,1] < thresh1_Low) and (indicators.iloc[i,2] < thresh2_Low):
               temp = [indicators.index.values[i],'IBM','SELL',self.unit]
               tempPos =- self.unit
            tempDate = dt.datetime.utcfromtimestamp(indicators.index.values[0].tolist()/1e9)
            daysBtwOrders  = tempDate - self.lastEntryDate
            if (daysBtwOrders.days > self.holdingPer) and (abs(tempPos) <= self.maxHoldings) and tempPos != self.position:
                orders.append(temp)
                self.position = tempPos
        orders = pd.DataFrame(orders,columns = ['Date','Symbol','Order','Shares'])
        return orders


test =  pd.DataFrame([[1,2,3]])
test2 = [1,2,3]


#getOrders(test2)
