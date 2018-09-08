import sys
sys.path.append('../segmentation/')
import labeller
import blobDetection
import os
from time import sleep
from os import system
#import cPickle
import showMitoticNucleus
import patch
import cv2 as cv
from time import time
def getPercentage(i,total):
    percentage = (float(i+1))/(float(total))
    percentage *= 10000
    percentage = int(round(percentage))
    percentage /= 100
    percentage = str(percentage)
    return percentage
def msg(message):
    f = open('status.xml','w')
    message = "<msg>"+message+"</msg>"
    f.write(message)
    f.close()
def segment(imagename,csvfile,destinaton):
    totalDataset = []
    msg('starting blobDetection and the image is '  + imagename)
    sleep(3)
    bloblist = blobDetection.segment(imagename)
	#print("bloblist",bloblist)
	#print("creating patches of the images")
	#t = time()
	#imagelist = patch.patch(imagename,bloblist,True)
	#t = time() - t
	#print("Time taken for patching is " +str(t) + "secs")
	#imagelist = []
	#print("fetching the coordinates of mitotic nuclues from the .csv files in dataset")
    msg('fetching mitotic nuclei')
    t = time()
    mitoticcentroidlist = showMitoticNucleus.getCentroidList(csvfile)
    t = time() - t
	#print("Time taken for fetching mitotic nuclei is " +str(t) + "secs")
	#print("labelling the images")
    msg('labelling and the size of mitotic nuclei is ' +str(len(bloblist)))
    sleep(2)
    t = time()
    mitotic_list,nonmitotic_list,misCount = labeller.labeller(bloblist,mitoticcentroidlist)
    t = time() - t
	#print("Time taken for Labelling is " +str(t) + "secs")
    msg('creating image patches')
    t = time()
    mitotic_imagelist = patch.patch(imagename,mitotic_list,True)
    nonmitotic_imagelist = patch.patch(imagename,nonmitotic_list,False)
    t = time() -t
	#print("Time taken for patching images is " +str(t)+"secs")
    msg('saving images and the size is ')
    for i in range(len(mitotic_imagelist)):
        address = "/var/www/html/Models-Comparison-Cls-Imb/pp/segmented_data/mitotic/img_"
        address += str(mitotic_list[i][0])+"_"+str(mitotic_list[i][1]) + "_"
        address +=  str(i) + ".jpg"
        cv.imwrite(address,mitotic_imagelist[i])

    for j in range(len(nonmitotic_imagelist)):
        d = str(nonmitotic_list[j])
        address = "/var/www/html/Models-Comparison-Cls-Imb/pp/segmented_data/non_mitotic/img_"
        address += str(nonmitotic_list[i][0])+"_"+str(nonmitotic_list[i][1]) + "_"
        address +=  str(j) + ".jpg"
        #command = "mv "+address+" ./segmented_data/non_mitotic/"
        cv.imwrite(address,nonmitotic_imagelist[j])
        #system(command)
        #msg(address+str(nonmitotic_imagelist[j].shape))
        percentage = getPercentage(j,len(nonmitotic_imagelist))
        msg("Saving segmented non-mitotic images"+ str(percentage) +"%")
        sleep(0.001)
	#print('misCount',misCount)
    #msg('images saved to '+destinaton)
    return misCount
