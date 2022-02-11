import unicorn_binance_websocket_api
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///hayda.db')

symbols = pd.read_csv('symbols.csv').to_list()
print('symbolsss')
print(symbols)
exit()

ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(['kline_1m'], ['btcusdt', 'bnbusdt'], output="UnicornFy")


def sql_import(data):
    time = data['event_time']
    ticker = data['symbol']
    price = data['kline']['close_price']
    frame = pd.DataFrame([[time, price]], columns=['time', 'price'])
    frame.time = pd.to_datetime(frame.time, unit='ms')
    frame.price = frame.price.astype(float)
    frame.to_sql(ticker, engine, index=False, if_exists='append')


while True:
    oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
    if oldest_data_from_stream_buffer:
        if oldest_data_from_stream_buffer.get('event_time') is not None:
            # price = oldest_data_from_stream_buffer.get('price')
            # if price is not None:
            #     print(f"Price = {price}")
            sql_import(oldest_data_from_stream_buffer)
            # print(oldest_data_from_stream_buffer)
