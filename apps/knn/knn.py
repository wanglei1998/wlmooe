import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as KNN
class knn:
    def courseclassTest(arr):
        data = pd.read_csv('./apps/knn/test.csv',encoding='gb2312')
        print(data)
        X = data[['点击量', '评分']]
        y = data['分类']
        knn_model = KNN(3)
        knn_model.fit(X,y)
        X_test = np.array([arr])
        y_test = knn_model.predict(X_test)
        print(y_test)
        return y_test

if __name__ == '__main__':
    print(knn.courseclassTest([10,4.9]))