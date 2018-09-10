import pickle as pkl
import numpy as np
from keras.models import load_model
def predict(pklAddress):
    (x_train, y_train), (x_test, y_test) = pkl.load(open(pklAddress,'rb'))
    x = np.append(x_train,x_test,axis=0)

    y = np.append(y_train,y_test,axis=0)
    print(x.shape)
    print(y.shape)
    model = load_model('../cost_sensitive/cost_sensitive.h5')
    y_pred = model.predict(x)
    l = []
    for i in y_pred:
        #print(i)
        i = np.argmax(i)
        l.append(i)
    l = np.asarray(l)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(l.shape[0]):
        if(l[i] == 1 and y[i] == 1):
            tp += 1
        if(l[i] == 0 and y[i] == 1):
            fn += 1
        if(l[i] == 1 and y[i] == 0):
            fp += 1
        if(l[i] == 0 and y[i] == 0):
            tn += 1
    print("tp",tp)
    print("tn",tn)
    print("fn",fn)
    print("fp",fp)
    return(tp,tn,fp,fn)
#pklAddress = '../../processed_dataset/dataset2.pkl'
#predict(pklAddress)
