import pickle as pkl
import os
import cv2 as cv
import numpy as np
from random import shuffle
def get_data(folder,type,label,mitotic_files,di):
    x = []
    y = []
    lst = []
    count = 0
    for imageAddress in mitotic_files:
        img = cv.imread(folder+di[type]+"/"+imageAddress)
        lst.append((img,label))
    shuffle(lst)
    #print(lst)
    mitotic_x = []
    mitotic_y = []
    for data in lst:
        x,y = data
        mitotic_x.append(x)
        mitotic_y.append(y)
    leng = len(mitotic_x)
    train = round(2*leng/3)
    test = leng - train
    #print("test",test)
    #print("train",train)
    x_train = np.asarray(mitotic_x[0:train])
    y_train = np.asarray(mitotic_y[0:train])
    x_test = np.asarray(mitotic_x[train:leng])
    y_test = np.asarray(mitotic_y[train:leng])
    return x_train,y_train,x_test,y_test
def create_pickle(folder,pickleDestination):
    di = []
    for dirpath,dirnames,filenames in os.walk(folder):
        #print(rn)
        dirnames.sort()
        di = dirnames
        break
    #print(di)
    mitotic_files = []
    for dirpath,dirnames,filenames in os.walk(folder+di[0]):
        mitotic_files = filenames
        break
    non_mitotic_files = []
    for dirpath,dirnames,filenames in os.walk(folder+di[1]):
        non_mitotic_files = filenames
        break
    mx_train,my_train,mx_test,my_test = get_data(folder,0,1,mitotic_files,di)
    m_dataset = (mx_train,mx_test)
    nx_train,ny_train,nx_test,ny_test = get_data(folder,1,0,non_mitotic_files,di)
    n_dataset= (nx_train,nx_test)
    pkl.dump(m_dataset,open(pickleDestination+"mitotic.pkl","wb"))
    pkl.dump(n_dataset,open(pickleDestination+"non_mitotic.pkl","wb"))
    print(mx_train.shape,nx_train.shape)
    x_train = np.append(mx_train,nx_train,axis=0)
    y_train = np.append(my_train,ny_train,axis = 0)
    x_test = np.append(mx_test,nx_test,axis = 0)
    y_test = np.append(my_test,ny_test,axis = 0)
    dataset = ((x_train,y_train),(x_test,y_test))
    pkl.dump(dataset,open(pickleDestination+"dataset2.pkl","wb"))
    print(x_train.shape,y_train.shape,x_test.shape,y_test.shape)
    return x_train,y_train,x_test,y_test
'''
folder = '../../segmented_data/'
x_train,y_train,x_test,y_test = create_pickle(folder)
print(x_train.shape,y_train.shape)
dataset = ((x_train,y_train),(x_test,y_test))
print(dataset)
pkl.dump(dataset,open("../../processed_dataset/dataset2.pkl","wb"))
'''
