import cv2
import numpy
#import cPickle
import preprocess
from console import delete_last_lines
import sys
pixelCount = 0
from time import time
from math import floor
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


def segment(imageName):
	'''img = cv2.imread(imageName)
	#print('in preprocess')
	img = preprocess.preprocess(img)
	cv2.imwrite("image.jpg",img)'''


	'''a = img.shape[0]
	b = img.shape[1]
	#blob detection\
	#print(numpy.amax(img))
	#print(a,b)
	visited = numpy.zeros((a,b))
	blobsList = []
	count = 0

	for i in range(1,a-1):
		for j in range(1,b-1):
			t = str(a*(i-1)+j)+"/"+str(a*b)
			#t = round((float(i*j)/float(a*b))*100)/100
			print(t+"% completed")

			delete_last_lines(1)
			if visited[i][j] == 0 and img[i][j] > 0:
				#count += 1
				#print("flood filling blob no. "+str(count))
				blob = []
				visited[i][j] = 1
				floodFill(img,i,j,visited,0,blob)
				if(len(blob) > 100):
					blobsList.append(blob)
					count += 1'''
	t2 = time()
	img = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
	params = cv2.SimpleBlobDetector_Params()
	params.filterByConvexity = False
	params.filterByInertia = True
	params.minInertiaRatio = 0.4
	params.filterByArea = True
	params.minArea = 15
	params.filterByColor = True
	params.blobColor = 255
	# Set up the detector with default parameters.
	detector = cv2.SimpleBlobDetector_create(params)
	# Setup SimpleBlobDetector parameters.

	# Detect blobs.
	blobsList = []
	print(type(img))
	keypoints = detector.detect(img)
	t2 = time() - t2
	print(str(t2)+"secs")
	blobsList = keypoints
	print("keypoints",len(keypoints))
	im_with_keypoints = cv2.drawKeypoints(img, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	# Show keypoints
	bloblist = []
	cv2.imwrite("Keypoints.jpg", im_with_keypoints)
	print(len(keypoints))
	for i in range(len(keypoints)):
		pt = keypoints[i].pt;
		x = pt[1]
		y = pt[0]
		x = int(floor(x))
		y = int(floor(y))
		#print(x,y)
		blobsList.append((x,y))
	l = len(keypoints)

	b = len(blobsList)
	blobsList = blobsList[round(b/2):b]
	print(len(blobsList))
	#cv2.waitKey(0)
	#import numpy as np
	#pts = np.float([keypoints[idx].pt for idx in len(keypoints)]).reshape(-1, 1, 2)
	#blobsList = getCentroids(blobsList)
	return blobsList
