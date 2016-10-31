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

def getCoeff(row,coeffChoice, coeffThresh):
    coeff = []
    for i in range(0,len(coeffChoice)):
        if row[i] < coeffThresh[i]:
            coeff.append(coeffChoice[i][0])
        else:
            coeff.append(coeffChoice[i][1])
    return coeff

def best4RT():
    Y = []
    X = np.random.choice(range(0,2000),size = (500,4),replace=True)
    coefChoice = [[0.5,2],[4,6],[6,8],[8,10]]
    coefThresh = [1000,1000,1000,1000]
    for i in range(0,X.shape[0]):
        x = np.array(X[i])
        coeffs = np.array(getCoeff(X[i],coefChoice,coefThresh))
        y = x * coeffs
        y = y.sum()
        Y.append(y)
    Y = np.array(Y)

    return X, Y

'''
if __name__=="__main__":
    print "they call me Tim."
'''

best4LinReg()
best4RT()
