import sys
import os
import segment
sys.setrecursionlimit(2000)
for dirpath,dirnames,filenames in os.walk("dataset"):
	dirnames.sort()
	count = 0
	for d in dirnames:
		files = []
		for dp,dn,fn in os.walk("dataset/"+d):
			fn.sort()
			for i in range(0,len(fn),3):
				imageName = "dataset/"+d+"/"+fn[i]
				print(imageName)
				count += 1
				csvName = "dataset/"+d+"/"+fn[i+1]
				print("segmenting image no."+str(count) +"/50")

				#print(imageName)
				#segment.segment(imageName,csvName,i)
				break
			break
		print("completed the folder" + d)
		break
