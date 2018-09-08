import numpy as np


def tp(y_true,y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	return true_positives
def recall(y_true, y_pred):
  true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
  possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
  recall = true_positives / (possible_positives + K.epsilon())
  return recall
def precision(y_true, y_pred):
  true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
  predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
  precision = true_positives / (predicted_positives + K.epsilon())
return precision

def f_measure(y_true, y_pred):
  def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

  def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision
  precision = precision(y_true, y_pred)
  recall = recall(y_true, y_pred)
return 2*((precision*recall)/(precision+recall+K.epsilon()))


def get_data():
  (x_train,y_train) = pkl.load(open("mitotic.pkl","rb"))
  (p_train,q_train) = pkl.load(open("non_mitotic.pkl","rb"))
   
  n1 =len(x_train)/3
  n2 = len(p_train)/3
  
  a_test = x_train[2*n1:]
  x_train = x_train[:2*n1]
  b_test = y_train[2*n1:]
  y_train = y_train[:2*n1]
  
  a_test.extend(p_train[2*n2:])
  p_train = p_train[:2*n2]
  b_test.extend(q_train[2*n1:])
  q_train = q_train[:2*n1]
  
  x_train.extend(p_train)
  y_train.extend(q_train)
  
  return x_train, y_train, (a_test, b_test)

def get_model():
  
 
	input_shape = (80,80,3)
	model = Sequential()
	#add zero padding to the input 
	model.add(Conv2D(256, (8, 8), input_shape=input_shape, strides=2))
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
	model.add(Dense(2),activation = 'soft-max')

	model.compile(loss='binary_crossentropy',
		      optimizer='rmsprop',
		      metrics=['accuracy', f_measure, tp]) 
	
	return model


(x_train, y_train),  test_data = get_data()

for i, l in enumerate(y_train):
  if y_train[i] == 0:
    y_train[i] = -1
   

y_train = to_catogorical(y_train, 2)
test_data[1] = to_catogorical(test_data[1],2)

x_train = x_train.astype('float32') / 255.
test_data[0] = test_data[0].astype('float32') / 255.


wts = np.asarray([1/len(x_train) for i in range(len(x_train))])

def train(wts):
  model = get_model()
  model.fit(x_train, y_train, sample_weight=wts, epochs=no_epochs
            ,validation_data = test_data)
  return model.train()

def adaboost_train(Nboost):
  C = []  
  alpha = []
  for i in range(Nboost):

    c = train(wts)
    c.save("ada_save/"+str(i)+".h5")
    C.append(c);

    
    Yhat = c.predict(x_train)
    e  = sum([wts[i] for i in range(len(wts)) if y_train[i]!=Yhat[i]])
    a = 0.5*log(1-e)/e
    alpha.append(a)

    p = -1*a*np.dot(y_train*Yhat)
    wts  = np.dot(wts*np.exp(p))
    wts = wts/np.sum(wts)

   
def predict(x, C, alpha):

  result = []
  for img in x:
    predict = np.asarray([c.predict(img) for c in C])
    
    for i, al in enumerate(alpha):
      predict[i] = predict[i]*al
      
    p1 = 0
    p2 = 0
    
    for i in range(len(predict)):
      p1+=predict[i][0]
      p2+=predict[i][1]
     
    if p1 > p2:
       res = -1
    else
       res = 1
    
    result.append(res):
  return np.asarray(result)


   
C,alpha = adaboost_train(10)
y = test_data[1]



def accuracy(y,yhat):
  return len([0 for i in range(y) if(y[i]!=yhat[i])])
  


p = precision(y_train, yhat)
r = recall(y_train, yhat)
f = 2*p*r/(p+r)
a = accuracy(y, yhat)




pkl.dump(open("ada_save/results.pkl",'wb'))
  
  
