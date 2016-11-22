

import pandas as pd
import numpy as np
import datetime as dt
import time as time
import os
from util import get_data, plot_data
import rule_based
import indicators
import analysis
import cProfile
import re

def calcBookMV(book,date):
    for i in range(0,book.shape[0]):
        price = get_data([book.ix[i,'Symbol']], pd.date_range(date,date),addSPY=False)
        price = price.iloc[0,0]
        if price/price == 1:
            book.ix[i,'Price'] = price
        book.ix[i,'Value'] = book.ix[i,'Price'] * book.ix[i,'Position']

    return book

def updateBook(book,order,cash,thresh=3.0):
    originalBook = book.iloc[:,:]
    signDict = {'SELL':-1,'BUY':1}
    if order['Symbol'] in book['Symbol'].tolist():
        idx = book.ix[book['Symbol']==order['Symbol'],'Position'].index.tolist()
        book.ix[idx,'Position'] = book.ix[idx,'Position'] + order['Shares']*signDict[order['Order']]

    else:
        order = order.tolist()
        newRow = [order[1],order[3]*signDict[order[2]],0,0]
        newRow = pd.DataFrame([newRow],columns=book.columns.values)
        book = pd.concat([book,newRow],ignore_index=True)

    price = get_data([order[1]], pd.date_range(order[0].to_datetime(),order[0].to_datetime()),addSPY=False)
    price = price.iloc[0,0]
    if price/price == 1:
        outCash = -1*signDict[order[2]] * order[3] * price +cash
    else:
        book = originalBook
        outCash = cash

    return book,outCash

def isOverLevered(book,cash, thresh):
    leverage = float(book['Value'].abs().sum()) / float(book['Value'].sum() + cash)
    #print('leverage')
    #print(leverage)
    if leverage > 3.0:
        return True
    else:
        return False

def compute_portvals(orders, start_val = 1000000):
    # this is the function the autograder will call to test your code
    #TODO: Your code here
    #FIXME: ??

    cash = start_val

    #orders = pd.read_csv(orders_file,sep=',',parse_dates = [0], infer_datetime_format=True)
    lastOrderRow = orders.shape[0]

    startDate = orders.ix[0,'Date']
    endDate = orders.ix[lastOrderRow-1,'Date']
    datesIndex = pd.date_range(startDate,endDate,freq='1D').tolist()
    spy = get_data(['SPY'],datesIndex,addSPY=False)
    newDates =spy.index.values
    for i in range(0,len(newDates)):
        temp= (newDates[i]- np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        newDates[i]=dt.datetime.utcfromtimestamp(temp)

    portVals = pd.DataFrame(index=newDates,columns=['Value'])
    lastPortRow = portVals.shape[0]

    book = pd.DataFrame(columns=['Symbol','Position','Price','Value'])

    for day in portVals.index.values:
        #print('Date')
        #print(day)
        originalBook = book.iloc[:,:]
        originalCash = cash
        for i in range(0,lastOrderRow):
            if pd.Timestamp(day).to_pydatetime() == orders.ix[i,'Date'].to_datetime():
                order = orders.ix[i,:]
                book = calcBookMV(book,day)
                book,cash = updateBook(book,order,cash)

        book = calcBookMV(book,day)
        #print('Current Book')
        #print(book)
        if isOverLevered(book,cash,3.0):
            book = originalBook
            cash = originalCash

        portV = book['Value'].sum()
        #print(portV)

        mv = portV + cash
        #print('Final MV')
        #print(mv)
        portVals.ix[day,'Value']=mv


    return portVals

def simulate_Orders(orders,sv = 1000000):


    # Process orders
    portvals = compute_portvals(orders = orders, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    start_date = orders.ix[0,'Date']
    end_date = orders.ix[orders.shape[0]-1,'Date']
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio,end_value = analysis.assess_portfolio(sd=start_date,ed=end_date,syms=['IBM'],allocs=[1])
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

def mapYFromReturn(prices, lookFwd, sellTresh=0, buyThresh=0):
    Y = prices.copy()
    Y.iloc[:,0]=np.nan
    labels =  Y.copy()
    print(prices)
    for i in range(0,prices.shape[0]-lookFwd):
        Y.iloc[i,0] = float(prices.iloc[i+lookFwd,0] - prices.iloc[i,0])/prices.iloc[i,0]
        if Y.iloc[i,0] >= buyThresh: labels.iloc[i,0] = 1
        elif Y.iloc[i,0] <=sellTresh: labels.iloc[i,0] = -1
        else: labels.iloc[i,0] = 0
    print(Y)
    print(labels)
    return labels


#CMD
start_date = dt.datetime(2008,1,1)
end_date = dt.datetime(2012,1,1)
datesIndex = pd.date_range(start_date,end_date,freq='1D').tolist()
symbols = ['IBM']
IBM_Data = get_data(symbols,datesIndex,addSPY=False)
IBM_Data= IBM_Data.dropna()
start = time.time()
MACD = indicators.getMACDValues(IBM_Data,20,5,10)
RSI = indicators.getRSIValues(IBM_Data,20)
indicator = pd.concat([MACD,RSI], axis = 1, join='inner')
print('full indicator data',indicator)

#end1 = time.time()
#print('Indicator time',end1-start)

orders = rule_based.getOrders(indicator,rule_based.ruleSTD,**{'sigmas':2})

#end1 = time.time()
#print('Indicator time',end1-start)
#print(orders)

#simulate_Orders(orders)

#end1 = time.time()
#print('Indicator time',end1-start)

#cProfile.run('re.compile("simulate_Orders|orders")')

Y = mapYFromReturn(IBM_Data,5)
print('Y',Y)

full_data = pd.concat([Y,indicator],axis = 1, join='inner')
