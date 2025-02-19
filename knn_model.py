import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier as KNN

print('Pandas Practice')

fraud_df = pd.read_csv('fraud_test_synthetic/fraudTrain.csv')
test_df = pd.read_csv('fraud_test_synthetic/fraudTrain.csv')

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