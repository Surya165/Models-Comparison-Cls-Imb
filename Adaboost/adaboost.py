import pickle as pkl
import keras
from keras.models import Sequential
from keras.utils import to_categorical
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
from math import log
no_epochs = 3
def tp(y_true,y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	return true_positives
def recall(y_true, y_pred):
  true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
  possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
  recall = true_positives / (possible_positives + K.epsilon())
  return recall
def precision(y_true, y_pred):
  true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
  predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
  precision = true_positives / (predicted_positives + K.epsilon())
  return precision

def f_measure(y_true, y_pred):
  def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

  def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision
  precision = precision(y_true, y_pred)
  recall = recall(y_true, y_pred)
  return 2*((precision*recall)/(precision+recall+K.epsilon()))




input_shape = (80,80,3)



def get_data_random():

  x = []
  y = []
  for _ in range(100):
    x.append(np.random.randint(0,255, input_shape))

  for _ in range(100):
    y.append(np.random.randint(2))

  x = np.asarray(x)
  y = np.asarray(y)

  a = x[70:]
  b = y[70:]
  x = x[:70]
  y = y[:70]
  return x,y,[a,b]


def get_data2():
  (x_train,y_train) = pkl.load(open("../../processed_dataset/mitotic.pkl","rb"))
  (p_train,q_train) = pkl.load(open("../../processed_dataset/non_mitotic.pkl","rb"))

  x_train = x_train.astype('float32') / 255.
  #x_test = x_test.astype('float32') / 255.
  n1 =len(x_train)/3
  n2 = len(p_train)/3

  a_test = x_train[2*n1:]
  x_train = x_train[:2*n1]
  b_test = y_train[2*n1:]
  y_train = y_train[:2*n1]

  a_test.extend(p_train[2*n2:])
  p_train = p_train[:2*n2]
  b_test.extend(q_train[2*n1:])
  q_train = q_train[:2*n1]

  x_train.extend(p_train)
  y_train.extend(q_train)

  return x_train, y_train, [a_test, b_test]
def get_model():
	model = Sequential()
  #add zero padding to the input
	model.add(Conv2D(1, (8, 8), input_shape=input_shape, strides=2))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(1, (8, 8)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.5))
	model.add(Conv2D(1, (4, 4)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.5))
	model.add(Flatten())
	model.add(Dense(1))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(2))
	model.add(Activation('softmax'))
	model.compile(loss='binary_crossentropy',optimizer='rmsprop', metrics=['accuracy'])
	return model

def get_data():
	####### inputing data
	x_train, y_train, (x_test, y_test) = get_data_random()








	#######


	y_train = keras.utils.to_categorical(y_train, 2)
	y_test =  keras.utils.to_categorical(y_test, 2)


	x_train = x_train.astype('float32') / 255.
	x_test = x_test.astype('float32') / 255.
	return x_train,y_train,x_test,y_test




def train(wts):
	model = get_model()
	x_train,y_train,x_test,y_test = get_data2()
	model.fit(x_train, y_train , sample_weight=wts, epochs=no_epochs
            ,validation_data = (x_train, y_train))
	return model





def predict(x, C, alpha):
	result = []
	for img in x:
		predict = np.asarray([c.predict(img.reshape(1,80,80,3)) for c in C])
		print(predict)
		for i, al in enumerate(alpha):
			predict[i] = predict[i]*al
		p1 = 0
		p2 = 0
		print(predict.shape)
		for i in range(len(predict)):
			p1+=predict[i][0][0]
			p2+=predict[i][0][1]
		res = 0
		if p1 > p2:
			res = -1
		else:
			res = 1
		result.append(res)
	return np.asarray(result)




def adaboost_train(Nboost):
	x_train,y_train,x_test,y_test = get_data2()
	C = []
	alpha = []
	for i in range(len(y_train)):
		if (y_train[i] == 0):
			y.append(-1)
		else:
			y.append(1)
	y = np.asarray(y)
	for i in range(Nboost):
		wts = np.asarray([1/len(x_train) for i in range(len(x_train))])
		c = train(wts)
		c.save("ada_save/"+str(i)+".h5")
		C.append(c)

		Yhat = c.predict(x_train)
		sum = 0
		for i in range(len(wts)):
			b = (y[i] != Yhat[i])
			if (b[0]):
				sum+=wts[i]
		e  = sum
		a = 0.5*(log(1-e))/(e+K.epsilon())
		alpha.append(a)
		q = -1*a
		p = y_train*Yhat
		p = np.dot(p,q)
		wts = np.dot(wts, np.exp(p))
		wts = wts/np.sum(wts)
	return C,alpha




#training
C,alpha = adaboost_train(3)



#scores
def test():
	x_train,y_train,x_test,y_test = get_data2()
	x = x_train
	print(y_train.shape)
	print(x_test.shape)
	yhat = predict(x, C, alpha)
	y = []
	for i in range(len(y_train)):
		if (y_train[i] == 0):
			y.append(-1)
		else:
			y.append(1)
	y = np.asarray(y)

	for i in range(yhat):
		if(yhat[i] == -1):
			yhat[i] = 0
	print(y.shape,yhat.shape)
	print(yhat)
	#p = precision(y, yhat)
	#r = recall(y, yhat)
	#f = 2*p*r/(p+r)
	#a = accuracy(y, yhat)

	#pkl.dump((p,r,f,a),open("ada_save/results.pkl",'wb'))
test()
