print('code running...')
import numpy as np
print('numpy imported')
import pandas as pd
print('pandas imported')
from sklearn.neighbors import KNeighborsClassifier as KNN
print('knn imported')

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)


# print('Check file exists')
# with open('fraudTrain.csv', 'r') as f_in:
#     for line in f_in:
#         print(line)

print('Pandas Practice')

full_df = pd.read_csv('fraudTrain.csv')
fraud_df = pd.read_csv('fraudTrain.csv').head(100)
test_df = pd.read_csv('fraudTest.csv').head(100)

# print("last index where is_fraud is true:" + str(full_df.index[full_df['is_fraud']]))
print("indexes of rows where is_fraud is true:")
print(full_df.loc[full_df["is_fraud"], full_df[["trans_date_trans_time", "merchant", "is_fraud"]]])

print(fraud_df.head())
print(fraud_df.columns)
print(fraud_df.dtypes)
print(fraud_df['merchant'][:20])
print()

print("sklearn Attempt")

X = fraud_df[['lat', 'long']].values # placeholder features
y = fraud_df['is_fraud'].values

knn = KNN(n_neighbors=6)
knn.fit(X, y)

test_X = test_df[['lat', 'long']].values

print(knn.predict(test_X))

# returns first index where is_fraud is true: df.index[df['is_fraud']]
# reverse a dataframe: df.iloc[::-1]