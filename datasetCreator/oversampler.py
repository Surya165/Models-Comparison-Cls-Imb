import cv2 as cv
import pickle as pkl
import numpy as np
def augment(arr):
    lis = []
    for i in range(arr.shape[0]):
        #rotate 1
        r1 = np.rot90(arr[i],1)
        r2 = np.rot90(arr[i],2)
        r3 = np.rot90(arr[i],3)
        #flip
        f1 = np.flip(arr[i],axis=0)
        f2 = np.flip(arr[i],axis=1)

        #rotation of flips
        rf1 = np.rot90(f1,1)
        rf2 = np.rot90(f2,1)
        lis.extend([r1,r2,r3,f1,f2,rf1,rf2])
    lis = np.asarray(lis)
    arr = np.append(arr,lis,axis=0)
    return arr

def oversample(folder):
    mTrain,mTest = pkl.load(open(folder+"mitotic.pkl","rb"))
    mTrain = augment(mTrain)
    mTest = augment(mTest)
    dataset = (mTrain,mTest)
    pkl.dump(dataset,open(folder+"oversampled_mitotic.pkl","wb"))
    nTrain,nTest = pkl.load(open(folder+"non_mitotic.pkl","rb"))
    nTrain = augment(nTrain)
    nTest = augment(nTest)
    dataset = (nTrain,nTest)
    pkl.dump(dataset,open(folder+"oversampled_non_mitotic.pkl","wb"))
folder = "../../processed_dataset/"
oversample(folder)
