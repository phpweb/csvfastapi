import requests
import json
import pandas as pd

path = 'all.csv'
url = requests.get("https://api.binance.com/api/v3/exchangeInfo")
text = url.text

data = json.loads(text)
symbols = [x for x in data['symbols'] if x['symbol'].endswith('USDT')]
symbols_data = []
for symbol in symbols:
    symbol = symbol['symbol']
    # symbol = symbol.str.contains('UP|DOWN', regex=True)
    symbols_data.append(symbol)
    # print(symbol['symbol'])
# print(symbols_data)
# symbols_data = symbols_data[~symbols_data.str.contains]
df = pd.DataFrame(symbols_data)
# df = df[~(df.str.contains('UP|DOWN', regex=True))]
# df = df[~df.stack().str.contains('UP|DOWN', regex=True)]
df = df[~df.stack().str.contains('UP|DOWN|TUSD').groupby(level=0).any()]
df.to_csv(path, mode='w', header=False, index=False)
print('before write')
print(len(df))
read_csv = pd.read_csv(path, header=None)
print('after read csv')
print(len(read_csv))

