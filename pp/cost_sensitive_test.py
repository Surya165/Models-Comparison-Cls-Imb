import sys
sys.path.append('..')
from cost_sensitive.predictor import predict
tp,tn,fp,fn = predict('./processed_dataset/dataset2.pkl')
print("The Predicted mitotic count is ",tp+fp)
print("The Actual mitotic count is ",tp+fn)
