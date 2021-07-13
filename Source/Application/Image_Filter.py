from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import cv2 as cv

class Image_Filter(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.sum_delete_pixel = 0
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X_adj = []
        delete_pixel = np.zeros((X.shape[0],1), dtype = int)
        for i in range(len(X)):
            img = X[i].reshape((28, 28))
            # Xoa dong, cot trong
            index_col = np.any(img != 0, axis=0)
            img = img[:, index_col]
            index_row = np.any(img != 0, axis=1)
            img = img[index_row]
            data = cv.resize(img, dsize=(28, 28), interpolation=cv.INTER_CUBIC)
            data = data.reshape(X.shape[1])
            X_adj.append(data)
            delete_pixel[i] = 784 - img.shape[0]*img.shape[1]
        X_adj=np.array(X_adj)
        X_adj = X_adj.reshape(X_adj.shape[0],-1)
        self.sum_delete_pixel = np.sum(delete_pixel)
        return X_adj