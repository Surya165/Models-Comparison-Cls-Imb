import numpy as np
import cv2 as cv
def getOversampleIndices(i):
	m = 0
	for j in range(i+1):
		if( i <= j*j):
			m = j
			break
	indices = []
	j = int(round(j/2))
	for k in range(-j,j+1):
		for l in range(-j,j+1):
			indices.append((k,l))
	return indices

def dimensions(centroid,is_mitotic,i,oversampleIndices):
	height = centroid[0]-40 + oversampleIndices[i][0]
	width = centroid[1]-40 + oversampleIndices[i][1]
	k = 0
	is_mitotic = True
	if (height <= 0 ):
		if is_mitotic:
			height = 0
	if (width <=0):
		if is_mitotic:
			width = 0
	if (height + 80 >= 2084):
		if is_mitotic:
			height = 2000
	if ( width + 80 >= 2084):
		if is_mitotic:
				width = 2000
	return (height,width)
def patch(img_name,blob_list,is_mitotic,oversample=1):
	img = cv.imread(img_name)
	oversampleIndices = getOversampleIndices(oversample)
	#um_rows, num_cols = img.shape[:2]
	images_list = []
	#print num_rows,num_cols

	for count,centroid in enumerate(blob_list):
		#print("patching image number " + str(count))
		new_img = np.zeros((80,80,3))
		#print("Centroid " + str(blob_list))
		for i in range(oversample):
			height,width = dimensions(centroid,is_mitotic,i,oversampleIndices)
			if(height >=0 and height < 2084 and width >=0 and width < 2084):
				new_img = img[height:height+80,width:width+80]
				images_list.append(new_img)
		#print("saving image no"+str(count))
		#cv.imwrite("nucleus/images"+str(count)+".jpg",new_img)
		#num_rows, num_cols = new_img.shape[:2]
		#print num_rows,num_cols
	return images_list
