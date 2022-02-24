import requests
import json
import pandas as pd

path = 'all_busd.csv'
url = requests.get("https://api.binance.com/api/v3/exchangeInfo")
text = url.text

data = json.loads(text)
symbols = [x for x in data['symbols'] if x['symbol'].endswith('BUSD') and x['status'] == 'TRADING']
# symbols = [x for x in symbols['symbols'] if x['status'] == 'TRADING']

symbols_data = []
for symbol in symbols:
    symbol = symbol['symbol']
    symbols_data.append(symbol)
df = pd.DataFrame(symbols_data)
df = df[~df.stack().str.contains('UP|DOWN|TUSD|BULL|BEAR').groupby(level=0).any()]
df.to_csv(path, mode='w', header=False, index=False)
print('before write')
print(len(df))
read_csv = pd.read_csv(path, header=None)
print('after read csv')
print(len(read_csv))

