import cv2
import numpy
#import cPickle
import preprocess
from console import delete_last_lines
import sys
from os import system
pixelCount = 0
from time import time
from math import floor
def msg(message):
    f = open('status.xml','w')
    message = "<msg>"+message+"</msg>"
    f.write(message)
    f.close()
def getCentroids(blobsList):
	#centroid creation
	centroidList = []
	count = 0
	#print(blobsList[0][1])

	for blob in blobsList:

		y = len(blob)
		#print(blob)
		if y <=0:
			continue
		count += 1
		centroidX = 0
		centroidY = 0
		for point in blob:
			#img[point[0]][point[1]] = 128
			#print(point)
			centroidX += point[0]
			centroidY += point[1]
		if len(blob) == 0:
			blobsList.remove(blob)
			continue
		centroidX /= y
		centroidY /= y
		centroidX = int(round(centroidX))
		centroidY = int(round(centroidY))
		#print("centroid of blob no. " + str(count)+"is",(centroidX,centroidY))
		centroidList.append((centroidX,centroidY))
	#print("total blob count is "+str(count))
	return centroidList
def get_neighbors(i,j):
	neighbors = []
	for ix in range(3):
		for jx in range(3):
			if j != 0 or i != 0:
				n = [(i+ix,j+jx),(i-ix,j+jx),(i+ix,j-jx),(i-ix,j-jx)]
				neighbors.extend(n)
	s = set(neighbors)
	neighbors = list(s)
	return neighbors
def floodFill(img,i,j,visited,recursionCount,blob):
	global pixelCount
	recursionCount += 1
	if recursionCount >= sys.getrecursionlimit() - 100:
		sys.setrecursionlimit(recursionCount+100)
	if  i >= img.shape[0] - 3 or j >= img.shape[1] - 3 or i == 2 or j == 2 or img[i,j] == 0:
		return
	neighbors = [(i,j+1),(i,j-1),(i-1,j+1),(i-1,j),(i-1,j-1),(i+1,j),(i+1,j-1),(i+1,j+1)]
	#neighbors = get_neighbors(i,j)
	visited[i][j] = 1
	blob.append((i,j))
	count = 0
	for k in range(8):
		x = neighbors[k][0]
		y = neighbors[k][1]
		#print x, y, visited[x][y],img[x][y]
		if visited[x][y] == 0 and img[x][y] != 0:
			count += 1
			pixelCount += 1
			floodFill(img,x,y,visited,recursionCount,blob)
	if count == 0:
		return
	return
def blobDetector(img):
	params = cv2.SimpleBlobDetector_Params()
	params.filterByConvexity = False
	params.filterByInertia = True
	params.minInertiaRatio = 0.001
	params.filterByArea = True
	params.minArea = 15
	params.filterByColor = True
	params.blobColor = 255
	detector = cv2.SimpleBlobDetector_create(params)
	blobsList = []

	img = cv2.imread("/var/www/html/image.jpg", cv2.IMREAD_GRAYSCALE)
	keypoints = detector.detect(img)

	#im_with_keypoints = cv2.drawKeypoints(img, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	blobslist = []
	for i in range(len(keypoints)):
		pt = keypoints[i].pt;
		x = pt[1]
		y = pt[0]
		x = int(floor(x))
		y = int(floor(y))
		blobsList.append((x,y))

	return blobsList

def segment(imageName):
    msg('reading image')
    img = cv2.imread(imageName)
    msg('preprocessing image')
    img = preprocess.preprocess(img)
    cv2.imwrite("/var/www/html/image.jpg",img)
    msg('performing blob detection')
    blobsList = blobDetector(img)
    return blobsList
