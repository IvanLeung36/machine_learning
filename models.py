import pandas as pd
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('csvs/fraudTrain.csv')
test_df = pd.read_csv('csvs/fraudTest.csv')

# Making a new df with equal parts fraud and non-fraud (to reduce bias in model)
fraud_trans = df[df['is_fraud'] == 1]
non_fraud_trans = df[df['is_fraud'] == 0]

# using random sampling to get an equal number of non-fraud entries
len_fraud = len(fraud_trans)
rand_non_fraud = non_fraud_trans.sample(n=len_fraud, random_state=42)

balanced_df = pd.concat([fraud_trans, rand_non_fraud])
balanced_df = balanced_df.sort_values('unix_time').reset_index(drop=True)

# getting features
features = []

# one-hot encoding 'category'
balanced_df = pd.get_dummies(balanced_df, columns=['category'], drop_first=True)
test_df = pd.get_dummies(test_df, columns=['category'], drop_first=True)

# converting from bool to integer
for x in balanced_df:
    if 'category' in x:
        balanced_df[x] = balanced_df[x].astype(int)
        test_df[x] = test_df[x].astype(int)
        features.append(x)

features.append('amt')

# Print the features
print("Features used for training:", features)

# Splitting up into train and test variables
X_train = balanced_df[features].values
y_train = balanced_df['is_fraud'].values
X_test = test_df[features].values
y_test = test_df['is_fraud'].values

# kNN
knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(X_train, y_train)
knn_pred = knn.predict(X_test)

# Decision tree
tree = DecisionTreeClassifier()
tree.fit(X_train, y_train)
tree_pred = tree.predict(X_test)

# Saving models
joblib.dump(knn, 'knn_model.pkl')
joblib.dump(tree, 'decision_tree_model.pkl')