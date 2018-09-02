#@title autoencoder tester
from keras.models import load_model
import keras.backend as K
from keras.datasets import mnist
import tensorflow as tf
#from google.colab import files
from keras.layers import Input, Dense
from keras.models import Model
from cv2 import imwrite
from cv2 import imshow
from time import sleep
import os
import numpy as np
import _thread as thread
from time import time
from time import sleep
import sys

def delete_last_lines(n=1):
  CURSOR_UP_ONE = '\x1b[1A'
  ERASE_LINE = '\x1b[2K'
  for _ in range(n):
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)

def euclidean_distance_loss(y_true, y_pred):
    a = tf.subtract(y_true,y_pred)
    b = tf.multiply(a,a)
    c = tf.reduce_sum(b,[1])
    d = tf.sqrt(c)
    with tf.Session() as sess:
      result = sess.run(d)
    return result
class compositeModel:
  def __init__(self,n_model,p_model):
    self.n_model = n_model
    self.p_model = p_model
  def accuracy(self,test,label):
    n_result = self.n_model.predict(test)
    p_result = self.p_model.predict(test)

    n_loss = euclidean_distance_loss(test,n_result)
    p_loss = euclidean_distance_loss(test,p_result)

    a = n_loss
    a = tf.convert_to_tensor(a,dtype=tf.float32)

    a = tf.subtract(p_loss,n_loss)
    b = tf.sign(a)
    ones = np.ones(n_loss.shape)
    ones = tf.convert_to_tensor(ones,dtype=tf.float32)
    c = tf.add(ones,b)
    d = tf.scalar_mul(0.5,c)
    e = tf.reduce_sum(d)
    result = 0
    with tf.Session() as sess:
      result = sess.run(e)
    t = result
    f = n_loss.shape[0] -result
    if(label == 0):
      temp = t
      t = f
      f = temp
    return(t,f)


  def evaluate(self,n_test,p_test):

    #get n_test accuracy
    #get p_test accuracy
    fp,tn = self.accuracy(n_test,0)
    fn,tp = self.accuracy(p_test,1)
    #fp = f_measure(tp,tn,fp,fn)
    print("tp is "+str(tp))
    print("tn is "+str(tn))
    print("fp is "+str(fp))
    print("fn is "+str(fn))
    p = (tp)/(tp+fp)
    r = (tp)/(tp+fn)
    fp = (2*p*r)/(p+r)

    return fp


def get_image(img2):
  max = 0
  max2 = 0
  for i in range(28):
     for j in range(28):
        if max < img2[i][j]:
           max = img2[i][j]
        if(max2 < img_actual[i][j]):
          max2 = img_actual[i][j]
  img2 = img2.astype('float32') * (255. / max )
  return img2


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
t1 = time()
n_train,n_test = get_data(x_train_full,x_test_full,y_train,y_test,1,1)
p_train,p_test = get_data(x_train_full,x_test_full,y_train,y_test,1,1)
t2 = time()
print("Splitting Time " + str(t2-t1) + " seconds")
#load models
t1 = time()
print("Loading")
n_model = load_model('n_model_1:50.h5')
p_model = load_model('p_model_1:50.h5')
t2 = time()
print("Loading Time " + str(t2-t1)+ " seconds")

#create the composite predictor
composite_model = compositeModel(n_model,p_model)
t1 = time()
print("Evaluating")
f_measure = composite_model.evaluate(n_test,p_test)
t2 = time()
print("Evaluation Time: "+str(t2-t1)+"seconds")
print(f_measure)
