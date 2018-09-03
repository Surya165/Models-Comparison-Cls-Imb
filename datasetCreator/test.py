from segment import segment
from os import system
print("deleting")
system('rm -rf segmented_data/mitotic/*')
system('rm -rf segmented_data/non_mitotic/*')
print('deleted')
segment('./dataset/A01_00.bmp','./dataset/A01_00.csv',0)
