import requests
import pickle
import decimal
from os.path import exists
import os
from functools import lru_cache
from binance.client import Client
from binance.helpers import round_step_size

client = Client()


def get_current_price(symbol):
    url = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    data = url.json()
    return data['price'].rstrip('0').rstrip('.')


def calculate_win_los_percent_with_decimal(start_price, end_price):
    """It should work now"""
    price_diff = ((float(start_price) / float(end_price)) * 100.00) - 100.00
    return round(price_diff, 2)


def extract_balance_symbol_from_pair(pair):
    return pair[-4:]


def extract_ticker_symbol_from_pair(pair):
    return pair[:-4]


def calculate_win_los_percent(start_price, end_price):
    price_diff = (float(end_price) / float(start_price)) - 1
    price_diff = '{:.4f}'.format(price_diff)
    return price_diff


@lru_cache(maxsize=None)
def get_sym_filters(symbol):
    pair_info = client.get_symbol_info(symbol)
    if pair_info is not None:
        symbol_filters = {}
        for filters in pair_info["filters"]:
            if filters["filterType"] == "PRICE_FILTER":
                symbol_filters['price_tick_size'] = filters["tickSize"].rstrip('0').rstrip('.')
            if filters["filterType"] == "MIN_NOTIONAL":
                symbol_filters['min_notional'] = float(filters["minNotional"].rstrip('0').rstrip('.'))
            if filters["filterType"] == "LOT_SIZE":
                symbol_filters['min_quantity'] = float(filters["minQty"].rstrip('0').rstrip('.'))
                symbol_filters['quantity_step_size'] = float(filters["stepSize"].rstrip('0').rstrip('.'))
        return symbol_filters
    return None


def get_price_with_precision(current_price, price_precision):
    price = round_step_size(float(current_price), float(price_precision))
    # Find the decimal place to format
    price_precision = str(price_precision)[::-1].find('.')
    price = "{:.{}f}".format(price, price_precision)
    return price


def calculate_quantity(balance, current_price, precision):
    quantity = float(balance) / float(current_price)
    quantity = quantity - float(precision)
    target_quantity = round_step_size(quantity, float(precision))
    return float(target_quantity)


def write_sl_to_pickle_file(symbol, sl):
    file_path = f'sl_tmp/{symbol}.pkl'
    file = open(file_path, 'wb')
    data = {
        'symbol': symbol,
        'sl': sl
    }
    pickle.dump(data, file)
    file.close()


def write_bought_price_to_pickle_file(symbol, price):
    file_path = f'sl_tmp/buy_pr/{symbol}.pkl'
    file = open(file_path, 'wb')
    data = {
        'symbol': symbol,
        'bought_price': price
    }
    pickle.dump(data, file)
    file.close()


def read_bought_price_from_pickle_file(symbol):
    file_path = f'sl_tmp/buy_pr/{symbol}.pkl'
    file_exists = exists(file_path)
    if not file_exists:
        return False
    file = open(file_path, 'rb')
    data = pickle.load(file)
    file.close()
    if data['symbol'] == symbol:
        return data['bought_price']
    return False


def read_from_pickle_file(symbol):
    file_path = f'sl_tmp/{symbol}.pkl'
    file_exists = exists(file_path)
    if not file_exists:
        return False
    file = open(file_path, 'rb')
    data = pickle.load(file)
    file.close()
    if data['symbol'] == symbol:
        return True
    return False


def check_if_sl_exists(symbol):
    return read_from_pickle_file(symbol)


def remove_sl_pickle_file(symbol):
    file_path = f'sl_tmp/{symbol}.pkl'
    file_exists = exists(file_path)
    if file_exists:
        os.remove(file_path)


def remove_bought_price_pickle_file(symbol):
    file_path = f'sl_tmp/buy_pr/{symbol}.pkl'
    file_exists = exists(file_path)
    if file_exists:
        os.remove(file_path)
