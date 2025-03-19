import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px

full_df = pd.read_csv('csvs/fraudTrain.csv')
fraud_df = pd.read_csv('csvs/fraudTrain.csv').head(10000)
test_df = pd.read_csv('csvs/fraudTest.csv').head(10000)

print(fraud_df.head())
print(fraud_df.columns)
print(fraud_df.dtypes)

X = fraud_df[['amt', 'lat', 'long']].values
y = fraud_df['is_fraud'].values

lin_reg = LinearRegression()
lin_reg.fit(X, y)

print(f"Coefficients: {lin_reg.coef_}")
print(f"Intercept: {lin_reg.intercept_}")

test_X = test_df[['amt', 'lat', 'long']].values
test_predictions = lin_reg.predict(test_X)

test_predictions = np.clip(test_predictions, 0, 1)

print(f"Predictions: {test_predictions}")

test_df['predictions'] = test_predictions

fig = px.scatter(test_df, 
                 x='amt', 
                 y='predictions', 
                 color='is_fraud', 
                 labels={'amt': 'Transaction Amount', 'predictions': 'Predicted Fraud Probability'}, 
                 title='Actual vs Predicted Fraud Status by Transaction Amount',
                 color_discrete_map={0: 'blue', 1: 'red'},
                 category_orders={"is_fraud": [0, 1]})

fig.update_traces(marker=dict(size=12, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
fig.show()

fig.write_html('linear-regression.html')
print("Plot has been saved as 'linear-regression.html'. You can open it in a browser.")
