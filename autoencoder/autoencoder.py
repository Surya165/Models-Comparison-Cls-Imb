from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
import tensorflow as tf
adam = Adam(lr=1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.01, amsgrad=False)

import numpy as np
import pickle as pkl
import keras.backend as K


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
    autoencoder.compile(optimizer='rmsprop', loss='binary_crossentropy')
    return autoencoder

def trainModel(model,mx_train,mx_test,name):
    model.fit(mx_train, mx_train,
                epochs=1,
                batch_size=128,
                shuffle=True,
                validation_data=(mx_test, mx_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])
    model.save(name+".h5")
mitoticModel = get_model()
non_mitoticModel = get_model()
folder = '../../processed_dataset/'
mx_train,mx_test = pkl.load(open(folder+'mitotic.pkl','rb'))
nx_train,nx_test = pkl.load(open(folder+'non_mitotic.pkl','rb'))

trainModel(mitoticModel,mx_train,mx_test,"mitoticModel")
trainModel(non_mitoticModel,nx_train,nx_test,"nonMitoticModel")
