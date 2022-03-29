from binance.streams import ThreadedWebsocketManager
import tr_sockets as sym_soc
import utils as utils
from config import get_settings

api_key = get_settings().api_key
api_secret = get_settings().api_secret

twm = ThreadedWebsocketManager(api_key, api_secret)
# start is required to initialise its internal loop
twm.start()


def handle_user_socket_message(msg):
    if msg['e'] == 'executionReport':
        symbol = msg['s']
        if 'BUSD' in symbol:
            # Buy action
            if msg['S'] == 'BUY' and msg['X'] == 'FILLED':
                bought_price = msg['p']
                utils.write_bought_price_to_pickle_file(symbol, bought_price)
                sym_soc.start_trade_socket(symbol)
            # Cancel mini ticker trade socket
            if (msg['S'] == 'SELL' and msg['X'] == 'FILLED' and msg['o'] == 'LIMIT') \
                    or (msg['o'] == 'LIMIT_MAKER' and msg['X'] == 'FILLED') \
                    or (msg['o'] == 'STOP_LOSS_LIMIT' and msg['X'] == 'FILLED'):
                sym_soc.stop_trade_socket(symbol)
            print('yes only BUSD')
            print(msg)


d = {}


def start_user_socket():
    print('Starting user socket')
    d['user_socket'] = twm.start_user_socket(callback=handle_user_socket_message)


def stop_user_socket():
    print(f'Stopping user socket')
    twm.stop_socket(d['user_socket'])


start_user_socket()
