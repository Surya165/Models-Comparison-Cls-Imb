#@title autoencoders trainer
from keras.layers import Input, Dense
from keras.models import Model
from keras.datasets import mnist
from cv2 import imwrite
from cv2 import imshow
import os
from time import time
import numpy as np
import tensorflow as tf
import keras.backend as K
def get_model(x_train,x_test,ratio):
  input_img = Input(shape=(784,))
  encoded = Dense(128, activation='relu')(input_img)
  encoded = Dense(64, activation='relu')(encoded)
  encoded = Dense(32, activation='relu')(encoded)

  decoded = Dense(64, activation='relu')(encoded)
  decoded = Dense(128, activation='relu')(decoded)
  decoded = Dense(784, activation='sigmoid')(decoded)
  autoencoder = Model(input_img, decoded)
  autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

  autoencoder.fit(x_train, x_train,
                  epochs=100,
                  batch_size=int(250/ratio),#int(round(256/ratio)),
                  shuffle=True,
                  validation_data=(x_train, x_train))
  return autoencoder

def get_data(x_train_full,x_test_full,y_train,y_test,number,ratio):
  x_train = []
  x_test = []
  for i,x in enumerate(x_train_full):
    if(y_train[i] == number):
      x_train.append(x)
  for i,x in enumerate(x_test_full):
    if(y_test[i] == number):
      x_test.append(x)
  x_train = np.asarray(x_train)
  x_test = np.asarray(x_test)
  x_train = x_train.astype('float32') / 255.
  x_test = x_test.astype('float32') / 255.
  x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
  x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
  x_test = x_test[1:int(round(len(x_test)/ratio))]
  x_train = x_train[1:int(round(len(x_train)/ratio))]
  print(x_train.shape,x_test.shape)
  return (x_train,x_test)

#load data
(x_train_full, y_train), (x_test_full, y_test) = mnist.load_data()

#get train and test data
n_train,n_test = get_data(x_train_full,x_test_full,y_train,y_test,1,1)
p_train,p_test = get_data(x_train_full,x_test_full,y_train,y_test,1,1)

#create and train models
t1 = time()
n_model = get_model(n_train[0:int(len(n_train)/2)],n_test,1)
p_model = get_model(p_train[0:int(len(p_train)/2)],p_test,1)
t2 = time()
print("Training Time: "+ str(t2-t1)+" seconds")
t1 = time()
n_model.save("n_model_1:50.h5")
p_model.save("p_model_1:50.h5")
t2 = time()
print("Saving Time: " + str(t2-t1) + " seconds")
