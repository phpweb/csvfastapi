from binance import ThreadedWebsocketManager
import utils as utils
import bn_client_private as bn_private

twm = ThreadedWebsocketManager()
# start is required to initialise its internal loop
twm.start()


def handle_trade_socket_message(msg):
    # r_mng.watch_sl_tp(msg)
    symbol = msg['s']
    sl_data = utils.read_sl_price_from_pickle_file(symbol)
    sl_price = sl_data['sl']
    sl_order_id = sl_data['orderId']
    # sl_price = '3.41500000'
    # print(f'SL price = {sl_price}')
    current_price = msg['p']
    # print(f'Current price = {current_price}')
    if current_price < sl_price:
        # print('Current price SL den kücükkkkkkk')
        bn_private.cancel_order(symbol, sl_order_id)
        bn_private.place_market_order(symbol)


d = {}


def start_trade_socket(symbol):
    print(f'Starting {symbol}')
    d[f'{symbol}'] = twm.start_trade_socket(callback=handle_trade_socket_message, symbol=symbol)


def stop_trade_socket(symbol):
    print(f'Stopping {symbol}')
    socket_name = twm.getName()
    print(f'Socket name {socket_name}')
    if socket_name:
        twm.stop_socket(d[f'{symbol}'])
