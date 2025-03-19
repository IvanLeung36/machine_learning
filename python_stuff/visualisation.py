import pandas as pd
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio
import plotly.graph_objects as go

pio.renderers.default = "notebook"

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (10, 6)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

pd.options.display.max_rows = 20000
df = pd.read_csv('fraudTest.csv')             
df['is_fraud'] = df['is_fraud'].astype('bool')

df.columns = df.columns.str.strip()
print("Columns in dataset:", df.columns)  

df.rename(columns={'trans_date_trans_time': 'trans_date'}, inplace=True)

df['trans_date'] = pd.to_datetime(df['trans_date'])

fraud_counts = df.groupby(['trans_date', 'is_fraud']).size().unstack(fill_value=0)
fraud_counts.columns = ['Non-Fraudulent', 'Fraudulent']

plt.figure(figsize=(12, 6))
plt.plot(fraud_counts.index, fraud_counts['Non-Fraudulent'], label='Non-Fraudulent', color='grey', marker='o')
plt.plot(fraud_counts.index, fraud_counts['Fraudulent'], label='Fraudulent', color='green', marker='o')
plt.title('Fraud vs Non-Fraud Transactions Over Time')
plt.xlabel('Date')
plt.ylabel('Transaction Count')
plt.legend(title="Transaction Type")
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig("fraud_vs_nonfraud_over_time.png")
plt.show()
print("Plot saved as 'fraud_vs_nonfraud_over_time.png'.")

fig = go.Figure()
fig.add_trace(go.Scatter(x=fraud_counts.index, y=fraud_counts['Non-Fraudulent'],
                         mode='lines+markers', name='Non-Fraudulent', line=dict(color='grey')))
fig.add_trace(go.Scatter(x=fraud_counts.index, y=fraud_counts['Fraudulent'],
                         mode='lines+markers', name='Fraudulent', line=dict(color='green')))
fig.update_layout(title='Fraud vs Non-Fraud Transactions Over Time',
                  xaxis_title='Date', yaxis_title='Transaction Count')
fig.write_html("fraud_vs_nonfraud_over_time.html")
print("Plot saved as 'fraud_vs_nonfraud_over_time.html'. Open this file in your browser.")

print(df.info())
print(df.describe())