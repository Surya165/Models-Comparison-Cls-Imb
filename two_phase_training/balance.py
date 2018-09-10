from keras.models import load_model
from sklearn.cluster import KMeans
import pickle as pkl
import numpy as np
import sys
sys.path.append("..")
from segmentation import preprocess
from preprocess import blueRatioHistogram
def second(val):
  return val[1][0]
def getPredictionSortedList():
    folder = "../../processed_dataset/"
    #mTrain,mTest = pkl.load(open(folder+'mitotic.pkl','rb'))
    nTrain,nTest = pkl.load(open(folder+'non_mitotic.pkl','rb'))
    y_train1 = np.ones((nTrain.shape[0],1))
    y_train2 = np.zeros((nTrain.shape[0],1))
    y_train = np.append(y_train1,y_train2,axis=1)
    y_test1 = np.ones((nTest.shape[0],1))
    y_test2 = np.zeros((nTest.shape[0],1))
    y_test = np.append(y_test1,y_test2,axis=1)
    model = load_model('firstPhase.h5')
    y_predTrain = model.predict(nTrain)
    y_predTest = model.predict(nTest)
    y_pred = np.append(y_predTrain,y_predTest,axis=0)
    print(y_pred.shape)
    y_true = np.append(y_train,y_test,axis=0)
    print(y_true.shape)

    y_true = y_true[:,1:]
    y_pred = y_pred[:,1:]
    print(y_pred)
    error = np.absolute(np.subtract(y_true,y_pred))
    x = np.append(nTrain,nTest,axis=0)
    dataset = []
    for i in range(error.shape[0]):
      l = []
      l.append(i)
      l.append(error[i])
      l = tuple(l)
      dataset.append(l)
    dataset.sort(key=second)
    dataset = np.asarray(dataset)
    dataset = dataset[:,:1]
    dataset =  dataset.astype(int)
    l = []
    print(dataset)
    for i in range(dataset.shape[0]):
      l.append(x[int(dataset[i])])
    l = np.asarray(l)
    dataset = l
    return dataset
dataset = getPredictionSortedList()
kmeans = KMeans(n_clusters=(dataset.shape[0]/10)*4).fit(dataset)
print(dataset.shape)
