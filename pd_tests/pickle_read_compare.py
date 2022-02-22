import os
import time
import pandas as pd


start = time.time()
df = pd.read_pickle('BTCUSDT.pkl')
print(df)
print('last row')
print(df.iloc[-1]['Time'])
request_time = time.time() - start
print(f'time passed {request_time}')
