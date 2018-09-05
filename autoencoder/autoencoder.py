from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import tensorflow as tf
adam = Adam(lr=1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0001, amsgrad=False)

import numpy as np
import pickle as pkl
import keras.backend as K
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

def get_model():
    input_img = Input(shape=(80, 80, 3))  # adapt this if using `channels_first` image data format

    x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    # at this point the representation is (4, 4, 8) i.e. 128-dimensional

    x = Conv2D(16, (4, 4), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (4, 4), activation='relu', padding='same')(x)
    x = UpSampling2D((2,2))(x)
    x = Conv2D(64, (1,1), activation='relu')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = Model(input_img, decoded)
    autoencoder.compile(optimizer=adam, loss='mean_squared_error')
    return autoencoder
mitoticModel = get_model()
non_mitoticModel = get_model()
folder = '../../processed_dataset/'
(x_train, y_train), (x_test, y_test) = pkl.load(open(folder+'dataset2.pkl', 'rb'))
mx_train,mx_test = pkl.load(open(folder+'mitotic.pkl','rb'))
nx_train,nx_test = pkl.load(open(folder+'non_mitotic.pkl','rb'))

mitoticModel.fit(mx_train, mx_train,
                epochs=1,
                batch_size=128,
                shuffle=True,
                validation_data=(mx_test, mx_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])
'''non_mitoticModel.fit(nx_train, nx_train,
                epochs=2,
                batch_size=128,
                shuffle=True,
                validation_data=(nx_test, nx_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])'''
mitoticModel.save('mitoticModel.h5')
non_mitoticModel.save('non_mitoticModel.h5')
mx = np.append(mx_train,mx_test,axis=0)
nx = np.append(nx_train,nx_train,axis=0)
mitoticm = mitoticModel.predict(mx)
mitoticn = non_mitoticModel.predict(mx)
a = euclidean(mx,mitoticm)
b = euclidean(mx,mitoticn)
print(a.shape)
print(b.shape)
with tf.Session() as sess:
    a = sess.run(a)
    b = sess.run(b)

a = np.reshape(a,(a.shape[0],1))
b = np.reshape(b,(b.shape[0],1))
x_train = np.append(a,b,axis=1)
print(x_train.shape)
y_train = np.zeros(x_train.shape,dtype=np.float32)
print(y_train.shape)
for y in y_train:
    y[1] = 1.0
predictor = get_predictor()

predictor.fit(x_train,y_train,
                epochs=1,
                batch_size=128,
                shuffle=True,
                validation_data=(x_train,y_train))
mitoticm = mitoticModel.predict(nx)
mitoticn = non_mitoticModel.predict(nx)
a = euclidean(nx,mitoticm)
b = euclidean(nx,mitoticn)
print(a.shape)
print(b.shape)
with tf.Session() as sess:
    a = sess.run(a)
    b = sess.run(b)


a = np.reshape(a,(a.shape[0],1))
b = np.reshape(b,(b.shape[0],1))
x_train = np.append(a,b,axis=1)
print(x_train.shape)
y_train = np.zeros(x_train.shape,dtype=np.float32)
print(y_train.shape)
for y in y_train:
    y[1] = 0.0
predictor = get_predictor()

predictor.fit(x_train,y_train,
                epochs=1,
                batch_size=128,
                shuffle=True,
                validation_data=(x_train,y_train))
'''print(a.shape)
print(b.shape)
mitotic_x = np.append(a,b)
print(mitotic_x.shape)
#fn = mitoticModel.predict(nx)'''
