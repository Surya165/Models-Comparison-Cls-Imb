#@title cost_sensitive_medical

#from google.colab import files
from keras.models import Model
from keras.backend import binary_crossentropy
from keras.utils import to_categorical
from time import time
import numpy as np
from keras import utils as np_utils
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
import pickle as pkl

def get_model():
    input_shape = (80,80,3)
    model = Sequential()
	#add zero padding to the input
    model.add(Conv2D(128, (8, 8), input_shape=input_shape, strides=2))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(512, (8, 8)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Conv2D(1024, (4, 4)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy',
		      optimizer='rmsprop',
		      metrics=['accuracy'])
    return model
def trainFirstPhase():
    folder = "../../processed_dataset/"
    (x_train,y_train),(x_test,y_test) = pkl.load(open(folder+'dataset2.pkl','rb'))
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    print(x_train.shape,y_train.shape,x_test.shape,y_test.shape)

    #mTrain,mTest = pkl.load(open(folder+'mitotic.pkl','rb'))
    '''nTrain,nTest = pkl.load(open(folder+'non_mitotic.pkl','rb'))
    y_train1 = np.ones((nTrain.shape[0],1))
    y_train2 = np.zeros((nTrain.shape[0],1))
    y_train = np.append(y_train1,y_train2,axis=1)
    y_test1 = np.ones((nTest.shape[0],1))
    y_test2 = np.zeros((nTest.shape[0],1))
    y_test = np.append(y_test1,y_test2,axis=1)
    print(y_train.shape)'''
    model = get_model()
    model.fit(x_train,y_train,
    				epochs=5,batch_size=128,
    	            verbose = 1,
    	            shuffle=True,
    	            validation_data=(x_test, y_test))
    model.save('firstPhase.h5')
trainFirstPhase()
