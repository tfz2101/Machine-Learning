import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
#from pykalman import KalmanFilter
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf,pacf, adfuller
from sklearn.cluster import KMeans
from Momentum_Module import Signals_Testing as myST
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingClassifier

from pandas import TimeSeries

'''
DATA_PATH = "L:\Trade_Data.xlsx"
TAB_NAME = "Temp_Data"
file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)

tst = np.array([1,2,1,2,1,1,2,2,1,0,1,3,1,2,1,2,1,2,1,1,2,2,1,0,1,3,1,2])

tsy_data = data.loc[:,"Change (Close to Close)"]

tst_pd = pd.Series(tst)

data_traits =myST.getDataTraitsOnlyPValue(tsy_data,10)




DATA_PATH = "L:\Trade_Data.xlsx"
TAB_NAME = "Data"
file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)

corr, matches = myST.calcSignalCorrelation(data)
print(corr)
print(matches)

hrs = myST.getNBlockHitRatio(data.iloc[:,0],30)
'''


'''
WRITE_PATH = "L:\Trade_Output.xlsx"
WRITE_PATH2 = "L:\Trade_Output2.xlsx"
TAB = 'Output'


data = data_traits.iloc[1:data_traits.shape[0],:]

kmeanstst = myST.kmeans_best_fit_cluster(data)
print(kmeanstst)
print(myST.kmeans_best_fit_cluster_labels(data))

data_traits =myST.getDataTraitsOnlyPValue(tsy_data,20)
print(data_traits)
acfs = data_traits['Autocorrelation'].values
acfs2 = myST.acf_fcn(acfs,lags=10)
print(pd.DataFrame(acfs2))


DATA_PATH = "L:\Trade_Data.xlsx"
TAB_NAME = "two_signals"
file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)
data = data.dropna(axis=0)
print(data)
'''


'''
Y = data['Change (Open to Open)'].values
X = data.drop('Change (Open to Open)',axis=1).values
model = myST.getSKLearnModel(Y,X,GradientBoostingRegressor)
cv_score = myST.getCrossValScore(model,Y, X, 20)
print(cv_score)
print(cv_score.mean())
'''



DATA_PATH = "L:\Trade_Data.xlsx"
TAB_NAME = "ML_Data"
WRITE_PATH = "L:\Trade_Output3.xlsx"
TAB = 'Output'


file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)

X = data['Change'].values
X = X[~np.isnan(X)]

X = np.array([1,2,3,5,1,1,1,1,3,0,1,4,6,7,8,9])
acf = myST.acf_fcn(X,5,.05)

pp = myST.pp_test_fcn(X,10)

df = myST.dickeyfuller_fcn(X,10)

rolling_data = data.drop('Yield',axis=1)
rolling_data = rolling_data.dropna(axis=0,how='any')

#acf_args = {'lags':4, 'alpha':.05,'ith':3}
#acf_data = myST.rolling_data_fcn(rolling_data,myST.acf_fcn_ith_cor,30,**acf_args)

acf_args = {'maxlag':3}
acf_data = myST.rolling_data_fcn(rolling_data,myST.pp_test_fcn,gap=7,**acf_args)

acf_data = pd.DataFrame(acf_data)

#print(acf_data)
#myST.write(acf_data,WRITE_PATH,TAB)



TAB_NAME = "Temp_Data"
file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)

data = data.dropna(axis=1)
