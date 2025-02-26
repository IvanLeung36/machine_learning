import pandas as pd

pd.options.display.max_rows = 20000
df = pd.read_csv('fraudTest.csv')

print(df)