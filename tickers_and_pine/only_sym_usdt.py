import os
import requests
import json
import pandas as pd
project_path = os.path.dirname(__file__) + '/'
path = project_path + 'all_usdt.csv'
url = requests.get("https://api.binance.com/api/v3/exchangeInfo")
text = url.text

data = json.loads(text)
symbols = [x for x in data['symbols'] if x['symbol'].endswith('USDT')]
symbols_data = []
for symbol in symbols:
    # print(symbol['symbol'] + ' = ' + symbol['status'])
    if symbol['status'] == 'TRADING':
        symbol = symbol['symbol']
        symbols_data.append(symbol)
df = pd.DataFrame(symbols_data)
# reg_ex = 'UP|DOWN|TUSD|BULL|BEAR'
# df = df[~df.stack().str.contains(reg_ex).groupby(level=0).any()]
df.to_csv(path, mode='w', header=False, index=False)
print('before write')
print(len(df))
read_csv = pd.read_csv(path, header=None)
print('after read csv')
print(len(read_csv))
total = len(read_csv)
max_item = total / 40

