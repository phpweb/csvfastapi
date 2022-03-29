from os.path import exists
import pickle
import utils as utils
import bn_client_private as bn_private
import bn_client_no_async as bn_public

last_sl_price = {
    'price': 0.0,
    'sl_1': False,
    'sl_2': False,
    'sl_3': False,
}


def watch_sl_tp(msg):
    symbol = msg['s']
    bought_price = utils.read_bought_price_from_pickle_file(symbol)
    # bought_price = 89.20
    if bought_price is not False:
        current_price = msg['p']
        print(f'Bought price from pickle file = {bought_price}')
        print(f"Current price: {current_price}")
        percent_win_or_lose = utils.calculate_win_los_percent(bought_price, current_price)
        if float(percent_win_or_lose) >= 0.0015 and last_sl_price['sl_1'] is False:
            print('yes it is more than 0.0002')
            update_oco_order(symbol)
            last_sl_price['price'] = float(current_price)
            last_sl_price['sl_1'] = True
        if float(percent_win_or_lose) >= 0.0030 and last_sl_price['sl_2'] is False:
            print('yes it is more than 0.0002')
            update_oco_order(symbol)
            last_sl_price['price'] = float(current_price)
            last_sl_price['sl_2'] = True

        if float(percent_win_or_lose) >= 0.0045 and last_sl_price['sl_3'] is False:
            print('yes it is more than 0.0002')
            update_oco_order(symbol)
            last_sl_price['price'] = float(current_price)
            last_sl_price['sl_3'] = True

        if float(percent_win_or_lose) <= -0.0030:
            bn_public.prepare_order(symbol, 'sell')
        print(f'percent_win_or_lose = {percent_win_or_lose}')
        print(f'last_sl_price = {last_sl_price}')


def reset_updated_sl_price():
    last_sl_price['price'] = 0.0
    last_sl_price['sl_1'] = False
    last_sl_price['sl_2'] = False
    last_sl_price['sl_3'] = False


def update_oco_order(symbol):
    sl_percent = 0.0015
    bn_private.get_sp_tp_order_and_cancel(symbol)
    tp_price = utils.read_tp_price_from_pickle_file(symbol)
    bn_public.prepare_oco_order(symbol, sl_percent=sl_percent, tp_price=tp_price)
