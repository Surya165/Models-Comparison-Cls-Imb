from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
adam = Adam(lr=0.00000001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0001, amsgrad=False)

import numpy as np
import pickle as pkl
def get_predictor():
    input_img = Input(shape=(2,))
    x = Dense(3)(input_img)
    x = Dense(2)(x)
    model = Model(input_img,x)
    x.compile(optimizer='adadelta',loss='binary_crossentropy',metrics=['acc'])
    return x

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
                epochs=300,
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
mx = np.append(mx_train,mx_test)
nx = np.append(nx_train,nx_train)
#tp = mitoticModel.predict(mx)
#fn = mitoticModel.predict(nx)
