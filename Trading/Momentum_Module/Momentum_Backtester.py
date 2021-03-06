import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
from pykalman import KalmanFilter
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf,pacf

DATA_PATH = "L:\Trade_Data.xlsx"
TAB_NAME = "Data"
SIGNAL_COL = "STD of Move"
ENTRY_COL ="IsEntry"
HIT_COL ="Hit Ratio for 1 HP"
DIRECTION_COL = "Direction"
CHANGE_COL = "Change"
PNL_COL = "Pnl"

file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)
data['Direction']=pd.Series(np.random.randn(data.shape[0]), index=data.index)


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


tst_data = data.iloc[:,0:1]
starting_point = [tst_data.iloc[0,0],0]
print("tst data",tst_data)

#Kalman Filter

tau = 0.1
kf = KalmanFilter(n_dim_obs=1,n_dim_state=2,
                  initial_state_mean=starting_point,
                  initial_state_covariance=np.eye(2),
                  transition_matrices=[[1,tau],[0,1]],
                  observation_matrices=[[1,0]],
                  observation_covariance=3,
                  transition_covariance=np.zeros((2,2)),
                  transition_offsets=[0,0])


np_data = tst_data["10y Close"].values

state_means, state_covs = kf.filter(np_data)
#tst_data['kf_predict']=pd.Series(state_means[:,0])
#print(state_means.shape)


times = np.arange(tst_data.shape[0])
plt.plot(times, state_means[:,0])
plt.plot(times, tst_data["10y Close"])

#plt.show()


tst_data['KF_Value']=state_means[:,0]
print("tst data",tst_data)

WRITE_PATH = "L:\Trade_Output.xlsx"
writer = pd.ExcelWriter(WRITE_PATH, engine='xlsxwriter')
tst_data.to_excel(writer, sheet_name='Data')
writer.save()


#Computes hit ratio for rolling n trades
def getLastNHitRatio(data, n, hitInd, acceptableValues):
    #@FORMAT: df[dates, hitOrNots]
    out = []
    temp = []
    count = 0
    for i in range(0,data.shape[0]):
        if data.iloc[i,hitInd] in acceptableValues:
            count = count +1
            temp.append(data.values[i,:])
        if count >= n:
            hr = np.average(temp,axis=0)[hitInd]
            out.append([data.values[i,0],hr])
            count = 0
            temp = []

    out = pd.DataFrame(out)
    #RETURNS: df[date, hit ratio for rolling n trades]
    return out

#Computes hit ratio for rolling n trades, computes for everyline
def getLastNHitRatioEveryLine(data, n, hitInd, acceptableValues):
    #@FORMAT: df[dates, hitOrNots]
    out = data.values
    avgs = np.empty((data.shape[0],1))
    avgs[:] = np.nan
    for i in range(0,data.shape[0]):
        count = 0
        temp = []
        j = i
        while j < data.shape[0]:
            if out[j,hitInd] in acceptableValues:
                count = count +1
                temp.append(out[j,:])
            if count >= n:
                hr = np.average(temp,axis=0)[hitInd]
                avgs[i]=hr
                break
            j = j +1

    print(avgs)
    out =  data.copy()
    out["Last Trades %"] = avgs
    print("out",out)
    #RETURNS: df[date, hit ratio for rolling n trades]
    return out


#Autocorrelation analysis
'''
DATA_PATH = "L:\Hit_Ratio_AR.xlsx"
TAB_NAME = "Data"
file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)

acceptableValues = [0,1]


#hr = getLastNHitRatio(data,15,3,acceptableValues)
#plt.plot(hr[1])
#plt.show()

hr2 = getLastNHitRatioEveryLine(data,15,3,acceptableValues)

WRITE_PATH = "L:\Hit_Ratio_AR.xlsx"
writer = pd.ExcelWriter(DATA_PATH, engine='xlsxwriter')
hr2.to_excel(writer, sheet_name='Output')
writer.save()


acf_fcn, confint,qstat,pvalues = acf(hr.iloc[:,1],nlags=10,qstat=True,alpha=0.05)
print("acf_fcn:",acf_fcn)
print("conf int",confint)
print("q",qstat)
print("pvlaues",pvalues)
'''