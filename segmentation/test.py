from segment import segment
from os import system
print("deleting")
destinaton = "../../segmented_data/"
system('rm -rf '+str(destinaton)+'mitotic/*')
system('rm -rf '+str(destinaton)+'non_mitotic/*')
print('deleted')
folder = '../../dataset/A01_v2/'

segment(folder+'A01_00.bmp',folder + 'A01_00.csv',0,destinaton)
