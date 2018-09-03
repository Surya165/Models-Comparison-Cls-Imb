import csv
import cv2
import numpy
import blobDetection

def getCentroidList(csvFileName):
	with open(csvFileName, 'r') as csvfile:
        	spamreader = csv.reader(csvfile)
	        dataset = list(spamreader)




	clist = []


	for mitotic in dataset:
		count = 0
		centroid_x = 0
		centroid_y = 0
		#print mitotic
		blobsList = []
		blob = []
		for i in range(0,len(mitotic),2):
			mitotic[i] = int(mitotic[i])
			mitotic[i+1] = int(mitotic[i+1])
			blob.append((mitotic[i+1],mitotic[i]))
			count += 1
		blobsList.append(blob)

		#print("blobs",len(blobsList))
		#print blobsList
		clist.extend(blobDetection.getCentroids(blobsList))
		#print mitotic
	#print("clist",clist)
	return clist
