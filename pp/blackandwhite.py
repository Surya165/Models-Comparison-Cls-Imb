
#!/home/rathod/.local/lib/python3.5/site-packages
def msg(message):
    f = open('status.xml','w')
    message = "<msg>"+message+"</msg>"
    f.write(message)
    f.close()
msg(' ')
import cv2 as cv
msg('cv imported')
import sys
msg('sys imported')
import os
from time import sleep
from os import system

sys.path.append('..')
msg('Path appended')
msg('importing segmentation')
from segmentation import segment

#print('segmentation imported')
from segment import segment
msg('starting segmentation')
#sys('chmod 777 blackandwhite.jpg')
imageAddress = str(sys.argv[1])
#img = cv.imread(imageAddress)
#img = preprocess(img)
#msg(str(img.shape))
#cv.imwrite('/home/rathod/saving.jpg',img)
msg('removing mitotic')
system('rm -rf ./segmented_data/mitotic/*')
msg('removing nonmitotic')
system('rm -rf ./segmented_data/non_mitotic/*')

msg('reading image '+imageAddress)
n = len(imageAddress)
csvAddress = imageAddress[:n-3]+"csv"
msg('reading csv')
destinaton = "/var/www/html/Models-Comparison-Cls-Imb/pp/segmented_data/"
misCount = 0
#msg("misCount is "+(str(misCount)))
msg('starting segmentation')
misCount = segment(imageAddress,csvAddress,destinaton)
msg('end')
