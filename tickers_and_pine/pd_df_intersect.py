import os
import pandas as pd
# print(os.path.dirname(__file__))
project_path = os.path.dirname(__file__) + '/'

path = project_path + 'intersect.csv'
usdt = pd.read_csv(project_path + "all_usdt.csv", header=None)
busd = pd.read_csv(project_path + "all_busd.csv", header=None)
busd = busd[0].str.replace('BUSD', '')
usdt = usdt[0].str.replace('USDT', '')

busd_dif = busd.to_frame().merge(usdt.to_frame(), how='inner', indicator=False)
busd_dif[[0]] = busd_dif[[0]] + 'USDT'
busd_dif.to_csv(path, mode='w', header=False, index=False)
only_busd_tickers = busd.to_frame().merge(usdt.to_frame(), how='outer', indicator=True).loc[
    lambda x: x['_merge'] == 'left_only']
# print(busd_dif)
# print(only_busd_tickers['right_only'])
# print(only_busd_tickers)
only_busd_tickers[[0]] = only_busd_tickers[[0]] + 'BUSD'
only_busd_tickers[[0]].to_csv(path, mode='a', header=False, index=False)
print('works')
