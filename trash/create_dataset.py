import sys
import os
import segment
sys.setrecursionlimit(2000)
#i = int(input())
print('blah')
print(os.walk('dataset'))
for dirpath,dirnames,filenames in os.walk("dataset"):
	dirnames.sort()
	print(filenames,0)
	count = 0
    #d = dirnames[i]
	files = []
	print(filenames)
	print(dirnames)
	for dp,dn,fn in os.walk("dataset/"):
		fn.sort()
		for i in range(0,len(fn),3):
			imageName = "dataset/"+fn[i]
			count += 1
			csvName = "dataset/"+fn[i+1]
			print("segmenting image no."+str(count) +"/50")

				#print(imageName)
			segment.segment(imageName,csvName,i)
	print("completed the folder" + d)
