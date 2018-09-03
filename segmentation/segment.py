import labeller
import blobDetection
import os
#import cPickle
import showMitoticNucleus
import patch
import cv2 as cv
from time import time
def segment(imagename,csvfile,mama,destinaton):
	totalDataset = []
	#imagename = "actualImage.jpg"
	#csvfile = "A00_01.csv"
	#print("segmenting the image into images of nucleui")
	#print('in blobDetection')
	#print(imagename)

	bloblist = blobDetection.segment(imagename)
	#print("bloblist",bloblist)
	#print("creating patches of the images")
	#t = time()
	#imagelist = patch.patch(imagename,bloblist,True)
	#t = time() - t
	#print("Time taken for patching is " +str(t) + "secs")
	#imagelist = []
	#print("fetching the coordinates of mitotic nuclues from the .csv files in dataset")
	t = time()
	mitoticcentroidlist = showMitoticNucleus.getCentroidList(csvfile)
	t = time() - t
	print("Time taken for fetching mitotic nuclei is " +str(t) + "secs")
	#print("labelling the images")
	t = time()
	mitotic_list,nonmitotic_list,misCount = labeller.labeller(bloblist,mitoticcentroidlist)
	t = time() - t
	print("Time taken for Labelling is " +str(t) + "secs")
	#print(labeledlist)
	count = 0
	#print(len(mitotic_list))
	#print('size of the non_mitotic list is '+str(len(nonmitotic_list)))
	t = time()
	mitotic_imagelist = patch.patch(imagename,mitotic_list,True)
	nonmitotic_imagelist = patch.patch(imagename,nonmitotic_list,False)
	t = time() -t
	print("Time taken for patching images is " +str(t)+"secs")

	#print(len(mitotic_list),len(mitotic_imagelist))

	for i in range(len(mitotic_imagelist)):
		cv.imwrite(destinaton+"mitotic/" + "img" +str(mitotic_list[i])+ str(i) + ".jpg",mitotic_imagelist[i])

	for j in range(len(nonmitotic_imagelist)):
		cv.imwrite(destinaton+"non_mitotic/" + "img"+str(nonmitotic_list[j]) +str(j) + ".jpg",nonmitotic_imagelist[j])
	print('misCount',misCount)
