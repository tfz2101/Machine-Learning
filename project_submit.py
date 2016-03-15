import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression as LR
from sklearn.naive_bayes import GaussianNB as NB
from sklearn.ensemble import RandomForestClassifier as RF

#Basic data preprocessing
bmi = pd.ExcelFile("BMI2.xlsx")
data = bmi.parse("raw_data_2")
data = data[data['10y']!=0]
bmi = data
bmi['avgSignal'] =  bmi.drop('10y',axis=1).mean(axis=1,skipna=True)
bmi = bmi.fillna(0)



#Define the functions for Logistic Regression, Naive Bayes, and Random Forest. The iterate function does a rolling cross validation since the data is a time series.
def logReg(data,yind, xind):
    model = LR()
    Y = data.iloc[range(0,data.shape[0]),yind]
    X = data.iloc[range(0,data.shape[0]),xind]
    model.fit(X,Y)
    Z = model.predict(X.iloc[X.shape[0]-1,:])
    Z = Z.tolist()
    prob =  model.predict_proba(X.iloc[X.shape[0]-1,:])
    prob = prob.tolist()
    classes = model.classes_.tolist()
    output = [Z,prob, classes]
    return output

def iterateLogReg(data, yind, xind, lkbk):
#Use the data from 0 to N - lkbk to make predictions for  N-lkbk to N once at a time

    output = data.copy()
    output['Prediction'] =  pd.Series(np.nan,index=output.index)
    output['Prob'] =  pd.Series(np.nan,index=output.index)
    output['hit'] =  pd.Series(np.nan,index=output.index)
    for i in range(lkbk,output.shape[0]):
        res = logReg(data.iloc[range(i-lkbk,i)],yind, xind)
        output.ix[i,'Prediction'] = res[0][0]
        probidx = res[2].index(res[0][0])
        prob = res[1][0][probidx]
        output.ix[i,'Prob']=prob
        if res[0][0]==data.ix[i,'10y']:
            output.ix[i,'hit']= 1
        else: output.ix[i,'hit']=0
    return output


def nb(data,yind, xind):
    model = NB()
    Y = data.iloc[range(0,data.shape[0]),yind]
    X = data.iloc[range(0,data.shape[0]),xind]
    model.fit(X,Y)
    Z = model.predict(X.iloc[X.shape[0]-1,:])
    Z = Z.tolist()
    prob =  model.predict_proba(X.iloc[X.shape[0]-1,:])
    prob = prob.tolist()
    classes = model.classes_.tolist()
    output = [Z,prob, classes]
    return output

def iterateNB(data, yind, xind, lkbk):
    #Use the data from 0 to N - lkbk to make predictions for  N-lkbk to N once at a time
    output = data.copy()
    output['Prob'] =  pd.Series(np.nan,index=output.index)
    output['hit'] =  pd.Series(np.nan,index=output.index)
    for i in range(lkbk,output.shape[0]):
        res = nb(data.iloc[range(i-lkbk,i)],yind, xind)
        output.ix[i,'Prediction'] = res[0][0]
        probidx = res[2].index(res[0][0])
        prob = res[1][0][probidx]
        output.ix[i,'Prob']=prob
        if res[0][0]==data.ix[i,'10y']:
            output.ix[i,'hit']= 1
        else: output.ix[i,'hit']=0
    return output


def rforest(data,yind, xind):
    model = RF(n_estimators=3)
    Y = data.iloc[range(0,data.shape[0]),yind]
    X = data.iloc[range(0,data.shape[0]),xind]
    model.fit(X,Y)
    Z = model.predict(X.iloc[X.shape[0]-1,:])
    Z = Z.tolist()
    prob =  model.predict_proba(X.iloc[X.shape[0]-1,:])
    prob = prob.tolist()
    classes = model.classes_.tolist()
    output = [Z,prob, classes]
    return output

def iterateRForest(data, yind, xind, lkbk):
    #Use the data from 0 to N - lkbk to make predictions for  N-lkbk to N once at a time
    output = data.copy()
    output['Prob'] =  pd.Series(np.nan,index=output.index)
    output['hit'] =  pd.Series(np.nan,index=output.index)
    for i in range(lkbk,output.shape[0]):
        res = rforest(data.iloc[range(i-lkbk,i)],yind, xind)
        output.ix[i,'Prediction'] = res[0][0]
        probidx = res[2].index(res[0][0])
        prob = res[1][0][probidx]
        output.ix[i,'Prob']=prob
        if res[0][0]==data.ix[i,'10y']:
            output.ix[i,'hit']= 1
        else: output.ix[i,'hit']=0
    return output




#SIMPLE CASE - JUST USE THE AVERAGE SIGNAL ACROSS ALL THE FEATURES AS A TRADING SIGNAL
basecase  = bmi.copy()
THRES_SIMPLE = 1
basecase['Play?']=basecase.avgSignal.apply(lambda k: np.nan if abs(k)<THRES_SIMPLE else 1)
basecase['hitNumber'] = basecase['avgSignal']*basecase['Play?']*basecase['10y']
basecase['hitOrNot'] = basecase.hitNumber.apply(lambda k: np.nan if np.isnan(k) else np.nan if k==0 else 0 if k<0 else 1)

print(basecase)
print(basecase.mean(skipna=True))
print(basecase.count(axis=0))



#Functions to test out meta parameters , i.e, the lookback the period of the rolling cross validation and the
def testThresh(out, operator):
    res = pd.DataFrame(columns= ['threshold', 'hitratio','plays'])
    i = 0.50
    while i < 0.8:
        if operator == '>':
            out['Play?']=out.Prob.apply(lambda k: np.nan if k > i else np.nan if np.isnan(k) else 1)
        else:
            out['Play?']=out.Prob.apply(lambda k: np.nan if k < i else np.nan if np.isnan(k) else 1)
        out['filteredHit']=out['hit']*out['Play?']
        temp = pd.DataFrame([[i,out.filteredHit.mean(skipna=True),out.filteredHit.count()]],columns= ['threshold', 'hitratio','plays'])
        res = res.append(temp,ignore_index=True)
        i = i + .005
    return res


def testLkBK(bmi,fcn,thres,operator):
    i = 30
    res = pd.DataFrame(columns= ['lkbk', 'hitratio','plays'])
    while i < 80:
        out  = fcn(bmi,0,range(1,5),i)
        THRES = thres
        if operator == '>':
            out['Play?']=out.Prob.apply(lambda k: np.nan if k>THRES else np.nan if np.isnan(k) else 1)
        else:
            out['Play?']=out.Prob.apply(lambda k: np.nan if k<THRES else np.nan if np.isnan(k) else 1)
        out['filteredHit']=out['hit']*out['Play?']
        temp = pd.DataFrame([[i,out.filteredHit.mean(skipna=True),out.filteredHit.count()]],columns= ['lkbk', 'hitratio','plays'])
        res = res.append(temp,ignore_index=True)
        i = i + 1
    return res



#Use LogReg to maximize the  filteredHit statistic (the hit ratio) while keeping the number of trading signals generated.
#print(testLkBK(bmi,iterateLogReg,0.565,'>').sort(['hitratio','plays'],ascending=False))
out  = iterateLogReg(bmi,0,range(1,5),56) #39
#print(testThresh(out,'>').sort(['hitratio','plays'],ascending=False))


#Use Naive Bayes to maximize the  filteredHit statistic (the hit ratio) while keeping the number of trading signals generated.
#print(testLkBK(bmi,iterateNB,0.6,'>').sort(['hitratio','plays'],ascending=False))
out2  = iterateNB(bmi,0,range(1,5),65) #39
#print(testThresh(out2,'>').sort(['hitratio','plays'],ascending=False))

#Use LogReg to maximize the  filteredHit statistic (the hit ratio) while keeping the number of trading signals generated.
#print(testLkBK(bmi,iterateRForest,0.65,'<').sort(['hitratio','plays'],ascending=False))
out3  = iterateRForest(bmi,0,range(1,5),41) #39
#print(testThresh(out3,'<').sort(['hitratio','plays'],ascending=False))

