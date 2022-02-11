import pandas as pd

path = "/Users/r.gezer/Documents/htdocs/python/fastapi/csv/crypto_2022-02-08.csv"
df = pd.read_csv(path)
# df.loc[df['Oscillators Rating'] == 'Buy']]
df = df[df['Oscillators Rating'] == 'Buy']
df = df[df['Ticker'].str.endswith('USDT')]
# print(csv)
print(df)
