import numpy
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

import math
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.core import Activation, Dropout

from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence

def create_dataset(dataset, look_back=1):
	dataX = []
	for i in range(0,len(dataset)):
		a = dataset[i:(i+look_back),0:X.shape[1]]
		dataX.append(a)
	return numpy.array(dataX)


DATA_PATH = "C:/Users/Frank Zhi/Downloads/Trading_Input.xlsx"
TAB_NAME = "deep_learning"
writer = pd.ExcelWriter('dl_output.xlsx')


file  = pd.ExcelFile(DATA_PATH)
data = file.parse(TAB_NAME)
data = data.dropna(axis=0)

#scaler = MinMaxScaler(feature_range=(0, 1))

data=(data-data.mean())/data.std()


Y = data['Change'].values
#Y = scaler.fit_transform(Y)
X = data[['Fade_Momentum','Econ_Surprise','Equity_Returns','OI']].values
#X = scaler.fit_transform(X)

Y_TRAIN = Y[0:2500]
Y_TEST = Y[2500:len(Y)]

X_TRAIN = X[0:2500,:]
X_TEST = X[2500:len(X),:]


X_TRAIN = create_dataset(X_TRAIN)
X_TEST = create_dataset(X_TEST)

X_TRAIN = numpy.reshape(X_TRAIN, (X_TRAIN.shape[0],1,X_TRAIN.shape[2]))
X_TEST = numpy.reshape(X_TEST, (X_TEST.shape[0],1,X_TEST.shape[2]))


model = Sequential()
model.add(LSTM(units=4,input_shape=(1,X.shape[1])))


model.add(Dense(units=1))


model.compile(loss='mean_squared_error',optimizer='adam')

#Epochs is how many times the model cycles through the training data. Each subsequent epoch the model will
#have a different memory to judge the input data.

#Batch size = 1 means it is online training, taking the input data one at a time instead of looking a batch of sequence
#data at once. 
model.fit(X_TRAIN,Y_TRAIN,batch_size=1,epochs=10,verbose=2)


# make predictions
trainPredict = model.predict(X_TRAIN)
testPredict = model.predict(X_TEST)

predxls = pd.DataFrame(testPredict)
print(predxls)
predxls.to_excel(writer,'predicted')

actxls = pd.DataFrame(Y_TEST)
print(actxls)
actxls.to_excel(writer,'actual')
writer.save()

''''
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(Y_TRAIN[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(Y_TEST[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

#scores = model.evaluate(X_TRAIN, Y_TEST, verbose=0)

'''
