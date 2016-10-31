"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regresstion than random trees
def best4LinReg():
    X = np.random.choice(range(0,2000),size = (500,4),replace=True)
    coeff = np.array([1,2,3,4])
    coeff = np.reshape(coeff,(4,1))
    Y = np.dot(X,coeff)
    Y = Y.flatten()
    print(Y)
    return X, Y

def getCode(row,coeffChoice, coeffThresh):
    map = {'0000':1,'1000':2,'0100':3,'1100':4,'1110':5,'0010':6,'1010':7,'0110':8,'0001':9,'1001':10,'0101':11,'1101':12,'1111':13,'0011':14,'1011':15,'0111':16}
    code = ""
    for i in range(0,4):
        if row[i]>=1000:
            code =code + '1'
        else:
            code =code + '0'
    print('code')
    print(code)
    out = map[code]
    return out

def best4RT():
    Y = []
    X = np.random.choice(range(0,2000),size = (500,4),replace=True)
    #coefChoice = [[0.5,2],[4,6],[6,8],[8,10]]
    #coefThresh = [1000,1000,1000,1000]
    for i in range(0,X.shape[0]):
        x = np.array(X[i])
        #y = getCode(x,coefChoice,coefThresh)
        y = sum([i**2 for i in x])
        Y.append(y)
    Y = np.array(Y)

    return X, Y

'''
if __name__=="__main__":
    print "they call me Tim."
'''

best4LinReg()
best4RT()
