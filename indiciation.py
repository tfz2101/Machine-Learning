
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

getMACDValues(IBM_Data,5,2,3)

'''

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    #TODO: Your code here
    #FIXME: ??

    cash = start_val

    orders = pd.read_csv(orders_file,sep=',',parse_dates = [0], infer_datetime_format=True)
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

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/extras2/orders-leverage-3.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
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

'''
