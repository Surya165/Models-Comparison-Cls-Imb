#@title Blue Ratio Histogram and global thresholding
#from IPython.display import Image, display
import os
#print("1")
import cv2 as cv
#print("2")
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
#print("3")
from time import time
#print("4")
from skimage import filters
#print("5")
def blueRatioHistogram(img):
  t1 = time()
  #img = cv.imread('A00_01.jpg')
  red = img[:,:,2]
  blue = img[:,:,0]
  green = img[:,:,1]

  red = tf.convert_to_tensor(red)
  green = tf.convert_to_tensor(green)
  blue = tf.convert_to_tensor(blue)

  blue = tf.to_float(blue)
  red = tf.to_float(red)
  green = tf.to_float(green)
  #100 * b
  b100 = tf.multiply(blue,100.)

  #r+g
  r_g = tf.add(red,green)

  #r+g+b
  r_g_b = tf.add(r_g,blue)

  one = tf.constant([[1.]])

  #r+g+b+1
  r_g_b_1 = tf.add(r_g_b,one)

  #r+g+1
  r_g_1 = tf.add(r_g,one)

  #factor1 = (100*b)/(r+g+1)
  factor1 = tf.div(b100,r_g_1)

  #256
  t56 = tf.multiply(one,255.)

  #factor2 = 256/(r+g+b+1)
  factor2 = tf.div(t56,r_g_b_1)

  #brh = factor1*factor2
  brh = tf.multiply(factor1,factor2)
  #normalising brh and scaling to 256
  maxb =brh
  a = tf.reduce_max(maxb,[0,1])
  brh = tf.div(brh,a)
  brh = tf.multiply(brh,255.)
  brh = tf.round(brh)
  brh = tf.cast(brh,tf.int32)


  with tf.Session() as sess:
    brh = sess.run(brh)
    #equal = sess.run(equal)
    #maxa = sess.run(a)
  t2 = time()
  t = (t2 - t1)
  #print("Time taken is "+str(t)+"us")
  return brh

def globalThreshold(brh,threshold):
  #global thresholding
  cond = tf.less(brh,threshold)
  brh = tf.where(cond,tf.zeros_like(brh),tf.multiply(255,tf.ones_like(brh)))
  with tf.Session() as sess:
    brh = sess.run(brh)
  return brh
def otsu(img):
  th = filters.threshold_otsu(img)
  return th
def preprocess(img):
    #print("Creating Blue Ratio Histogram")
    img = blueRatioHistogram(img)
    #cv.imwrite('brh.jpg',img)
    #print("Calculating Otsu Threshold")
    threshold = otsu(img)
    #print('Global Thresholding')
    img = globalThreshold(img,threshold)
    kernel = np.ones((3,3), np.uint8)
    img = img* 1.0
    img = img.astype(np.float32)
    #print("Morphological operations")
    img = cv.dilate(img,kernel,iterations=1)
    img = cv.erode(img, kernel, iterations=3)

    return img
