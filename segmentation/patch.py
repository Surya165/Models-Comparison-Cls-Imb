import numpy as np
import cv2 as cv

def patch(img_name,blob_list,is_mitotic):
	img = cv.imread(img_name)

	#um_rows, num_cols = img.shape[:2]
	images_list = []
	#print num_rows,num_cols

	for count,centroid in enumerate(blob_list):
		#print("patching image number " + str(count))
		new_img = np.zeros((80,80,3))
		#print("Centroid " + str(blob_list))
		height = centroid[0]-40
		width = centroid[1]-40
		k = 0

		if (height <= 0 ):
			if is_mitotic:
				height = 0
			else:
				continue
		if (width <=0):
			if is_mitotic:
				width = 0
			else:
				continue
		if (height + 80 >= 2084):
			if is_mitotic:
				height = 2000
			else:
				continue
		if ( width + 80 >= 2084):
			if is_mitotic:
				width = 2000
			else:
				continue
		new_img = img[height:height+80,width:width+80]
		'''for i in range(height,height+80):
			l = 0
			for j in range(width,width+80):
				for s in range(3):
					new_img[k][l][s] = img[i][j][s]
				l+=1
			k+=1
		'''
		images_list.append(new_img)
		#print("saving image no"+str(count))
		#cv.imwrite("nucleus/images"+str(count)+".jpg",new_img)
		#num_rows, num_cols = new_img.shape[:2]
		#print num_rows,num_cols
	return images_list
