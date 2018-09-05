import cv2 as cv
import sys
import os
from time import sleep
from os import system
sys.path.append('..')
def msg(message):
    f = open('status','w')
    f.write(message)
    f.close()
msg('Path appended')
sleep(1)
from segmentation import segment
msg('imported segmentation')
#print('segmentation imported')
#from segment import segment
#sys('chmod 777 blackandwhite.jpg')
#system('rm -rf ./segmented_data/mitotic/*')
#system('rm -rf ./segmented_data/non_mitotic/*')
imageAddress = str(sys.argv[1])
n = len(imageAddress)
csvAddress = imageAddress[:n-3]+"csv"
destinaton = "./segmented_data/"
misCount = 0
#msg("misCount is "+(str(misCount)))
#misCount = segment(imageAddress,csvAddress,destinaton)
