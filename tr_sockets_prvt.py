from binance import ThreadedWebsocketManager, Client
import r_mng as r_mng
from config import get_settings

api_key = get_settings().api_key
api_secret = get_settings().api_secret

twm = ThreadedWebsocketManager(api_key, api_secret)
# start is required to initialise its internal loop
twm.start()


def handle_user_socket_message(msg):
    print(msg)


d = {}


def start_user_socket():
    print('Starting user socket')
    d['user_socket'] = twm.start_user_socket(callback=handle_user_socket_message)


def stop_user_socket():
    print(f'Stopping user socket')
    twm.stop_socket(d['user_socket'])
