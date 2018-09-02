#@title cost_sensitive_medical
from keras.models import load_model
import keras.backend as K
import pickle as pkl
from keras.datasets import mnist
import tensorflow as tf
#from google.colab import files
from keras.models import Model
from keras.backend import binary_crossentropy
from time import time
import numpy as np
from keras import utils as np_utils
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np




def get_model():
	input_shape = (80,80,3)
	model = Sequential()
	#add zero padding to the input
	model.add(Conv2D(256, (8, 8), input_shape=input_shape, strides=2))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Conv2D(512, (8, 8)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.5))
	model.add(Conv2D(1024, (4, 4)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.5))
	model.add(Flatten())
	model.add(Dense(1024))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(1))
	model.add(Activation('sigmoid'))

	model.compile(loss='binary_crossentropy',
		      optimizer='rmsprop',
		      metrics=['accuracy'])

	return model

def cost_sensitive(a,y):
  error = binary_crossentropy(a, y)
  error = K.mean(error,axis=-1)
  return error


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

(x_train, y_train), (x_test, y_test) = pkl.load(open('breast_cancer.pkl', 'rb'))


model = get_model()
model.compile(optimizer="adadelta",loss=cost_sensitive,metrics=['acc',f_measure])
c_weights = {}
c_weights[0] = 1.
c_weights[1] = 20
model.fit(x_train,y_train,
                epochs=100,
                batch_size=128,
                verbose = 1,
                shuffle=True,
                validation_data=(x_test, y_test),class_weight=c_weights)
