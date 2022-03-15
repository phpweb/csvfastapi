from binance import ThreadedWebsocketManager
import r_mng as r_mng

twm = ThreadedWebsocketManager()
# start is required to initialise its internal loop
twm.start()


def handle_trade_socket_message(msg):
    r_mng.watch_sl_tp(msg)
    # print(msg)


d = {}


def start_trade_socket(symbol):
    print(f'Starting {symbol}')
    d[f'{symbol}'] = twm.start_trade_socket(callback=handle_trade_socket_message, symbol=symbol)


def stop_trade_socket(symbol):
    print(f'Stopping {symbol}')
    twm.stop_socket(d[f'{symbol}'])
