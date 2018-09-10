import os
from os import system
from time import time
import sys
from math import floor
sys.path.append('..')
from segmentation import segment
from segment import segment
from pickleCreator import create_pickle
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'
def delete_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
destinaton = "../../segmented_data/"
folder = "../../dataset/"
command = "rm -rf "+destinaton
system(command+"mitotic/*")
system(command+"non_mitotic/*")
dis = []
for dirpath,dirnames,filenames in os.walk(folder):
    dis = dirnames
    break
print(dis)
fileNames = []
for d in dis:
    for dp,dn,fn in os.walk(folder+d):
        for f in fn:
            fileNames.append(folder+d+"/"+f)
        break

#print(fileNames)
fileNames.sort()
totalMisCount = 0
total = len(fileNames)/3
print("Started Segmentation")
totalTime = time()
n = len(fileNames)
avgTime = 0
for i in range(0,n,3):
    imagename = fileNames[i]
    csvfile = fileNames[i+1]
    t = time()
    misCount = segment(imagename,csvfile,destinaton,imagenumber=i,oversample=10 )
    totalMisCount += misCount
    print(str(int(i/3+1))+"/"+str(total)+" completed")
    t = time() - t
    t = round(t)
    t = int(t)
    avgTime *= (i/3)
    avgTime += t
    avgTime /= ((i/3) + 1)
    print("misCount is ",misCount)
    if(i == 0):
        print("E.T.A: Estimating ....")
    else:
        eta = (total - (i/3)-1 )*avgTime
        eta = int(round(eta))
        mins = str(int(round(eta / 60)))
        secs = str(eta % 60)
        print("E.T.A: "+mins+"m"+secs+"s")

    delete_last_lines(3)

totalTime = time() - totalTime
print("Total time taken: ",totalTime)
print("Total misCount is ",totalMisCount)
print("Creating Pickle")
folder = '../../segmented_data/'
pickleDestination = "../../processed_dataset/"
create_pickle(folder,pickleDestination)
print("pickle created")
