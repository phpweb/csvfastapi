import ccxt
import pandas as pd
import datetime
from binance.client import Client
from sqlalchemy import create_engine
from tqdm import tqdm

client = Client()

exch = 'binance'
symbol = 'BTC/USDT'
# coins = ('BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT', 'DOTUSDT', 'LUNAUSDT',
#          'DOGEUSDT', 'AVAXUSDT', 'SHIBUSDT', 'MATICUSDT', 'LTCUSDT', 'UNIUSDT', 'ALGOUSDT', 'TRXUSDT',
#          'LINKUSDT', 'MANAUSDT', 'ATOMUSDT', 'VETUSDT')

coins = ('BTCUSDT', 'ETHUSDT')

exchange_list = ['binance']
exchange = getattr(ccxt, exch)()
# exchange.load_markets()
t_frame = '1m'
timestamp = int(datetime.datetime.strptime("2022-02-21 11:20:00", "%Y-%m-%d %H:%M:%S").timestamp() * 1000)


# data = exchange.fetch_ohlcv(symbol, t_frame, timestamp)
# header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
# df = pd.DataFrame(data, columns=header)
# df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
# df.set_index('Timestamp')
# filename = '{}.csv'.format(t_frame)
# print(df)


def get_minute_data(symbol, lookback):
    data = exchange.fetch_ohlcv(symbol, t_frame, timestamp, 100000)
    data = exchange.fetch
    header = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = pd.DataFrame(data, columns=header)
    frame.Time = pd.to_datetime(frame.Time, unit='ms')
    return frame


def get_minute_data_bn(symbol, lookback):
    data = client.get_historical_klines(symbol, '1m', lookback + ' days ago UTC')
    frame = pd.DataFrame(data)
    frame = frame.iloc[:, :5]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    frame[['Time', 'Open', 'High', 'Low', 'Close']] = frame[['Time', 'Open', 'High', 'Low', 'Close']].astype('float')
    frame.Time = pd.to_datetime(frame.Time, unit='ms')
    return frame


engine = create_engine('sqlite:///PricesTest.db')

# df_ccx = get_minute_data('BTC/USDT', "1")
# df_bn = get_minute_data_bn('BTCUSDT', "1")
# print(df_ccx)
# print(df_bn)

# to sql
# for coin in tqdm(coins):
#     get_minute_data_bn(coin, '30').to_sql(coin, engine, index=False)

# to pickle
for coin in tqdm(coins):
    get_minute_data_bn(coin, '30').to_pickle(coin + '.pkl')
