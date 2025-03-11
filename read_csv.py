import pandas as pd
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio

pio.renderers.default = "notebook"

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (10, 6)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

pd.options.display.max_rows = 20000
df = pd.read_csv('fraudTest.csv')                   
df['is_fraud'] = df['is_fraud'].astype('bool')


fig = sns.histogram(df, 
                   x='city_pop', 
                   marginal='box', 
                   color='is_fraud', 
                   color_discrete_sequence=['green', 'grey'], 
                   title='City population against is_fraud')

fig.update_layout(bargap=0.1)
fig.show()
fig.write_html("city_pop_distribution_plot.html")
print(df)
print(df.info())
print(df.describe())
print("Plot saved as 'city_pop_distribution_plot.html'. Open this file in your browser.")
# Value against fraud or non fraud