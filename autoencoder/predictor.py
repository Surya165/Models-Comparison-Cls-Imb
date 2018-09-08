from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
import pickle as pkl
import keras.backend as K
from keras.models import load_model
adam = Adam(lr=1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0001, amsgrad=False)
def euclidean(y_true, y_pred):
    return K.sqrt(K.sum(K.square(y_pred - y_true), axis=[1,2,3]))

def get_predictor():
    input_img = Input(shape=(2,))
    x = Dense(100)(input_img)
    x = Dense(100)(x)
    x = Dense(2)(x)
    model = Model(input_img,x)
    model.compile(optimizer=adam,loss='binary_crossentropy',metrics=['acc'])
    return model
def getTrainDataForPredictor(trueModel,falseModel,x,label):
    tx = trueModel.predict(x)

    fx = falseModel.predict(x)

    tx = euclidean(x,tx)
    fx = euclidean(x,fx)

    with tf.Session() as sess:
        tx = sess.run(tx)
        fx = sess.run(fx)
    tx = np.reshape(tx,(tx.shape[0],1))
    fx = np.reshape(fx,(fx.shape[0],1))
    print(tx.shape,fx.shape)
    x_train = np.append(tx,fx,axis=1)
    y_train = []
    y_traina = []
    y_trainb = []
    if(label == 0):
        y_traina = np.zeros((x_train.shape[0],1))
        y_trainb = np.ones((x_train.shape[0],1))
        y_train = np.append(y_traina,y_trainb,axis=1)
    if(label == 1):
        y_traina = np.ones((x_train.shape[0],1))
        y_trainb = np.zeros((x_train.shape[0],1))
        y_train = np.append(y_traina,y_trainb,axis=1)
    return x_train,y_train
def getDistances(mitoticModel,nonMitoticModel,mx,nx):
    mx_train,my_train = getTrainDataForPredictor(mitoticModel,nonMitoticModel,mx[0:4],1)
    print(mx_train.shape,my_train.shape)
    nx_train,ny_train = getTrainDataForPredictor(nonMitoticModel,mitoticModel,nx[0:4],0)
    print(nx_train.shape,ny_train.shape)

    x_train = np.append(mx_train,nx_train,axis=0)
    y_train = np.append(my_train,ny_train,axis=0)
    return x_train,y_train
def train(folder):
    mx_train,mx_test = pkl.load(open(folder+'mitotic.pkl','rb'))
    nx_train,nx_test = pkl.load(open(folder+'non_mitotic.pkl','rb'))

    mx = np.append(mx_train,mx_test,axis = 0)
    nx = np.append(nx_train,nx_test,axis = 0)

    mitoticModel = load_model('mitoticModel.h5')
    non_mitoticModel = load_model('nonMitoticModel.h5')
    print(mx.shape)
    x_train,y_train = getDistances(mitoticModel,non_mitoticModel,mx,nx)
    print(x_train.shape,y_train.shape)

    predictor = get_predictor()

    predictor.fit(x_train,y_train,
                epochs=1,
                batch_size=128,
                shuffle=True,
                validation_data=(x_train,y_train))
    predictor.save('predictor.h5')
    return predictor
def test(folder):
        mx_train,mx_test = pkl.load(open(folder+'mitotic.pkl','rb'))
        nx_train,nx_test = pkl.load(open(folder+'non_mitotic.pkl','rb'))

        mx = np.append(mx_train,mx_test,axis = 0)
        nx = np.append(nx_train,nx_test,axis = 0)

        mitoticModel = load_model('mitoticModel.h5')
        non_mitoticModel = load_model('nonMitoticModel.h5')
        print(mx.shape)
        x_true,y_true = getDistances(mitoticModel,non_mitoticModel,mx,nx)
        print(x_true.shape,y_true.shape)
        predictor = load_model('predictor.h5')
        y_pred = predictor.predict(x_true)

        y_pred = np.argmax(y_pred,axis=1)
        y_true = np.argmax(y_true,axis=1)
        print(y_true)
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for i in range(y_pred.shape[0]):
            if(y_pred[i] == 1 and y_true[i] == 1):
                tp += 1
            if(y_pred[i] == 0 and y_true[i] == 1):
                fn += 1
            if(y_pred[i] == 1 and y_true[i] == 0):
                fp += 1
            if(y_pred[i] == 0 and y_true[i] == 0):
                tn += 1
        #predictor.save('predictor.h5')
        return (tp,tn,fp,fn)
tp,tn,fp,fn = test('../../processed_dataset/')
