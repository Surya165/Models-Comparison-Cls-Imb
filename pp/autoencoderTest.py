import sys
sys.path.append('..')
from autoencoder.predictor import test

tp,tn,fp,fn = test('./processed_dataset/')
print("The predicted mitotic count is ",tp+fp)
print("The actual mitotic count is ",tp+fn)
