print('code running...')
import numpy as np
print('numpy imported')
import pandas as pd
print('pandas imported')
# from sklearn.neighbors import KNeighborsClassifier as KNN
# print('knn imported')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

df = pd.read_csv('csvs/fraudTrain.csv')
print('dataframe read')

print(df.head())
print(df.columns)
print(df.dtypes)

print(df[['category', 'amt', 'first', 'last', 'is_fraud']].head())