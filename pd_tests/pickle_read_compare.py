import os
import time
import pandas as pd

pickle_path = os.path.realpath('') + '/pd_tests/BTCUSDT.pkl'
start = time.time()
df = pd.read_pickle(pickle_path)
print(df)
print('last row')
# Get last row as a series object
print(df.iloc[-1]['Time'])
# Get last row as a dataframe object
print(df.iloc[-1:]['Time'])
request_time = time.time() - start
print(f'time passed {request_time}')
