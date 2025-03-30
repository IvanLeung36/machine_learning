import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# Load datasets
df = pd.read_csv('csvs/fraudTrain.csv')
test_df = pd.read_csv('csvs/fraudTest.csv')

# Balance the dataset
fraud_trans = df[df['is_fraud'] == 1]
non_fraud_trans = df[df['is_fraud'] == 0]
len_fraud = len(fraud_trans)
rand_non_fraud = non_fraud_trans.sample(n=len_fraud, random_state=42)
balanced_df = pd.concat([fraud_trans, rand_non_fraud]).reset_index(drop=True)

# Extract hour from 'unix_time'
balanced_df['hour'] = pd.to_datetime(balanced_df['unix_time'], unit='s').dt.hour
test_df['hour'] = pd.to_datetime(test_df['unix_time'], unit='s').dt.hour

# One-hot encode 'category'
categories = df['category'].unique()
for category in categories:
    balanced_df[f'category_{category}'] = (balanced_df['category'] == category).astype(int)
    test_df[f'category_{category}'] = (test_df['category'] == category).astype(int)

balanced_df = balanced_df.drop(columns=['category'])
test_df = test_df.drop(columns=['category'])
test_df = test_df.reindex(columns=balanced_df.columns, fill_value=0)

# Define features
features = [col for col in balanced_df.columns if col.startswith('category_')] + ['hour', 'amt']
print(features)
# Split data into features and labels
X_train = balanced_df[features]
y_train = balanced_df['is_fraud']
X_test = test_df[features]
y_test = test_df['is_fraud']

# Train decision tree
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)

# Train kNN
knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(X_train, y_train)

# Save models and features
joblib.dump(tree, 'decision_tree_model.pkl')
joblib.dump(knn, 'knn_model.pkl')
joblib.dump(features, 'features.pkl')