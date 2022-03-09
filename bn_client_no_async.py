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
import utils

api_key = get_settings().api_key
api_secret = get_settings().api_secret
client = Client(api_key, api_secret)


def prepare_order(symbol, side):
    sym_filters = get_sym_filters(symbol)
    min_quantity = sym_filters['min_quantity']
    min_notional = sym_filters['min_notional']
    quantity_step_size = sym_filters['quantity_step_size']
    price_tick_size = sym_filters['price_tick_size']
    current_price = get_current_price(symbol)

    # current_price = 65.12232
    current_price_with_precision = get_price_with_precision(current_price, price_tick_size)
    quantity = 0
    order_side = ''
    if side == 'buy':
        asset_symbol = utils.extract_balance_symbol_from_pair(symbol)
        asset_balance = get_asset_balance(asset_symbol)
        if float(asset_balance) < float(min_notional):
            logger.error(f'Min notional is too small! {symbol}')
            return {"error": f"Min notional is too small! {symbol}"}
        quantity = calculate_quantity(asset_balance, current_price_with_precision, quantity_step_size)
        if float(quantity) < float(min_quantity):
            logger.error(f'Minimum quantity is not enough by BUY! {symbol}')
            return {"error": f"Minimum quantity is not enough by BUY! {symbol}"}
        order_side = SIDE_BUY
    if side == 'sell':
        ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
        symbol_balance = get_asset_balance(ticker_symbol)
        quantity = round_step_size(float(symbol_balance), float(quantity_step_size))
        if float(quantity) < float(min_quantity):
            logger.error(f'Minimum quantity is not enough by SELL! {symbol}')
            return {"error": f"Minimum quantity is not enough by SELL! {symbol}"}
        quantity = round_step_size(float(quantity), float(quantity_step_size))
        quantity = quantity - float(quantity_step_size)
        order_side = SIDE_SELL
    order_placed = create_order(symbol, order_side, quantity, ORDER_TYPE_LIMIT, current_price_with_precision)
    if order_placed:
        if order_placed['status'] == 'FILLED':
            print(f'Order {order_side} {symbol} successful.')
            if side == 'buy':
                # Persist this info for sale later
                sell_quantity = order_placed['executedQty']
                quantity = round_step_size(float(sell_quantity), float(quantity_step_size))
        if order_placed['status'] != 'FILLED':
            time.sleep(2)
            order_id = order_placed['orderId']
            order_status = is_order_filled(symbol, order_id)
            if order_status is False:
                terminate_order = cancel_order(symbol, order_id)
                if terminate_order:
                    prepare_order(symbol, side)
            if order_status is True:
                print(f'Order {order_side} {symbol} successful after second try.')
                if side == 'buy':
                    # Persist this info for sale later
                    sell_quantity = order_placed['executedQty']
                    quantity = round_step_size(float(sell_quantity), float(quantity_step_size))


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
    except BinanceAPIException as e:
        logger.error(f'{side} with {symbol}: ' + e.message)
    else:
        return order_send


def get_current_price(symbol):
    url = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    data = url.json()
    return data['price']


def get_price_with_precision(current_price, price_precision):
    return round_step_size(float(current_price), float(price_precision))


@lru_cache(maxsize=None)
def get_sym_filters(symbol):
    pair_info = client.get_symbol_info(symbol)
    symbol_filters = {}
    for filters in pair_info["filters"]:
        if filters["filterType"] == "PRICE_FILTER":
            symbol_filters['price_tick_size'] = filters["tickSize"].rstrip('0').rstrip('.')
        if filters["filterType"] == "MIN_NOTIONAL":
            symbol_filters['min_notional'] = filters["minNotional"].rstrip('0').rstrip('.')
        if filters["filterType"] == "LOT_SIZE":
            symbol_filters['min_quantity'] = filters["minQty"].rstrip('0').rstrip('.')
            symbol_filters['quantity_step_size'] = filters["stepSize"].rstrip('0').rstrip('.')
    return symbol_filters


def calculate_quantity(balance, current_price, precision):
    quantity = float(balance) / float(current_price)
    target_quantity = round_step_size(quantity, float(precision))
    # We subtract a little
    return float(target_quantity) - float(precision)


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


def is_order_filled(symbol, order_id):
    try:
        order = client.get_order(symbol=symbol, orderId=order_id)
        if order:
            print(order)
            status = False
            if order['status'] == 'FILLED' or order['status'] == 'CANCELED':
                status = True
            return status
    except BinanceAPIException as e:
        logger.error(e)
        print(e)


def cancel_order(symbol, order_id):
    try:
        return client.cancel_order(symbol=symbol, orderId=order_id)
    except BinanceAPIException as e:
        logger.error(e)
        print(e)


# start = time.time()
# prepare_order('LUNABUSD', 'buy')
# request_time = time.time() - start
# print(f'NO asyncio time spent = {request_time}')

# start = time.time()
# get_price_filter_tick_size('LUNABUSD')
# print(get_price_filter_tick_size.cache_info())
# request_time = time.time() - start
# print(f'NO asyncio time spent = {request_time}')
#
# start = time.time()
# get_price_filter_tick_size('LUNABUSD')
# print(get_price_filter_tick_size.cache_info())
# request_time = time.time() - start
# print(f'Second call asyncio time spent = {request_time}')


# prepare_order('LUNABUSD', 'sell')
# order_filled = is_order_filled('LUNABUSD', 458282764)
# print(order_filled)
# if order_filled is False:
#     print(cancel_order('LUNABUSD', 458246373))
