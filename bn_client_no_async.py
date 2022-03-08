import requests
import json
import asyncio
from functools import lru_cache
import time
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
from binance.helpers import round_step_size
from config import get_settings
from debug_log import logger

api_key = get_settings().api_key
api_secret = get_settings().api_secret
client = Client(api_key, api_secret)


def prepare_order(symbol, side):
    if side == 'buy':
        side = SIDE_BUY
    else:
        side = SIDE_SELL
    current_price = get_current_price(symbol)
    print(f'current price {current_price}')
    current_price = 65.0
    price_tick_size = get_price_filter_tick_size(symbol)
    asset_balance = get_asset_balance()
    quantity = calculate_quantity(asset_balance, current_price, price_tick_size)
    order_send = create_order(symbol, side, quantity, ORDER_TYPE_LIMIT, current_price)
    print(order_send)


def create_order(symbol, side, quantity, order_type, price):
    try:
        recv_window = 50000
        order_send = client.create_order(symbol=symbol,
                                         side=side,
                                         quantity=quantity,
                                         type=order_type,
                                         timeInForce=TIME_IN_FORCE_GTC,
                                         price=price,
                                         recvWindow=recv_window)
        print(f"SUCCESS: Real order - {side} is successful")
    except BinanceAPIException as e:
        logger.error(e)
        print(e)
    else:
        return order_send


def get_current_price(symbol):
    url = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    data = url.json()
    return data['price']


@lru_cache(maxsize=128, typed=False)
def get_price_filter_tick_size(symbol):
    pair_info = client.get_symbol_info(symbol)
    symbol_filters = {}
    for filters in pair_info["filters"]:
        if filters["filterType"] == "PRICE_FILTER":
            symbol_filters['price_tick_size'] = filters["tickSize"].rstrip('0').rstrip('.')
        if filters["filterType"] == "MIN_NOTIONAL":
            symbol_filters['min_national'] = filters["minNotional"].rstrip('0').rstrip('.')
        if filters["filterType"] == "LOT_SIZE":
            symbol_filters['min_quantity'] = filters["minQty"].rstrip('0').rstrip('.')
            symbol_filters['quantity_step_size'] = filters["stepSize"].rstrip('0').rstrip('.')
    return symbol_filters


def calculate_quantity(balance, current_price, precision):
    quantity = float(balance) / float(current_price) * float(0.9995)
    quantity = str(quantity)
    target_price = round_step_size(current_price, precision)
    return float(quantity[:quantity.find('.') + precision + 1])


def get_asset_balance(asset_name=''):
    balance_symbol = 'BUSD'
    if asset_name:
        balance_symbol = asset_name
    balance_resp = client.get_asset_balance(balance_symbol)
    balance = 0
    if balance_resp['asset'] == balance_symbol:
        balance = balance_resp['free']
        print(balance_resp['free'])
    return balance


@lru_cache()
def f():
    pass

# start = time.time()
# prepare_order('LUNABUSD', 'buy')
# request_time = time.time() - start
# print(f'NO asyncio time spent = {request_time}')

# start = time.time()
hasta = get_price_filter_tick_size('LUNABUSD')
print(get_price_filter_tick_size.cache_info())
# request_time = time.time() - start
# print(f'NO asyncio time spent = {request_time}')
print(f())
print(f.cache_info())
