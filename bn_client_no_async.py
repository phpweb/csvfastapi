import requests
import json
import asyncio
from decimal import Decimal, ROUND_DOWN
import math
from typing import Union
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
    if sym_filters is None:
        print('There is no such a sym.')
        return {"error": "There is no such a sym."}
    min_quantity = sym_filters['min_quantity']
    min_notional = sym_filters['min_notional']
    quantity_step_size = sym_filters['quantity_step_size']
    price_tick_size = sym_filters['price_tick_size']
    current_price = get_current_price(symbol)

    # current_price = 65.12232
    quantity = 0
    current_price_with_precision = 0
    order_side = ''
    if side == 'buy':
        asset_symbol = utils.extract_balance_symbol_from_pair(symbol)
        asset_balance = get_asset_balance(asset_symbol)
        # print(f'asset balance = {asset_balance} min notional = {min_notional}')
        if float(asset_balance) < float(min_notional):
            logger.info(f'Min notional is too small! {symbol}')
            return {"error": f"Min notional is too small! {symbol}"}
        current_price_with_precision = get_price_with_precision(current_price, price_tick_size)
        quantity = calculate_quantity(asset_balance, current_price_with_precision, quantity_step_size)
        # print(f'quantity {quantity} min quantity {min_quantity}')
        if float(quantity) < float(min_quantity):
            logger.info(f'Minimum quantity is not enough by BUY! {symbol}')
            return {"error": f"Minimum quantity is not enough by BUY! {symbol}"}
        order_side = SIDE_BUY
    if side == 'sell':
        ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
        symbol_balance = get_asset_balance(ticker_symbol)
        symbol_balance = float(symbol_balance) - float(quantity_step_size)
        quantity = round_step_size(float(symbol_balance), float(quantity_step_size))
        if float(quantity) < float(min_quantity):
            logger.info(f'Minimum quantity is not enough by SELL! {symbol}')
            return {"error": f"Minimum quantity is not enough by SELL! {symbol}"}
        current_price_with_precision = get_price_with_precision(current_price, price_tick_size)
        quantity = round_step_size(float(quantity), float(quantity_step_size))
        order_side = SIDE_SELL
    print(f'Current price with precision = {current_price_with_precision}')
    order_placed = create_order(symbol, order_side, quantity, ORDER_TYPE_LIMIT, current_price_with_precision)
    if order_placed:
        if order_placed['status'] == 'FILLED':
            print(f'Order {order_side} {symbol} successful.')
            if side == 'buy':
                after_buy_actions(order_placed, quantity_step_size, price_tick_size)
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
                    after_buy_actions(order_placed, quantity_step_size, price_tick_size)


def get_current_price(symbol):
    url = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    data = url.json()
    return data['price']


def after_buy_actions(order_placed, quantity_step_size, price_tick_size):
    # Persist this info for sale later
    symbol = order_placed['symbol']
    stop_price, price = calculate_stop_loss_prices(symbol, price_tick_size)
    ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
    symbol_balance = get_asset_balance(ticker_symbol)
    symbol_balance = float(symbol_balance) - float(quantity_step_size)
    quantity = round_step_size(float(symbol_balance), float(quantity_step_size))
    place_stop_loss_order(symbol, quantity, stop_price, price)


def calculate_stop_loss_prices(symbol, price_tick_size=None, percent=0.0007):
    # 0.01 means 1 percent
    # 0.005 means half of 1 percent
    # 0.0001 means 1 out of 1 percent
    if price_tick_size is None:
        sym_filters = get_sym_filters(symbol)
        if sym_filters is None:
            print('There is no such a sym.')
            return {"error": "There is no such a sym."}
        price_tick_size = sym_filters['price_tick_size']

    current_price = get_current_price(symbol)

    stop_loss_amount = float(current_price) * float(percent)
    stop_price = float(current_price) - stop_loss_amount

    stop_limit_price = stop_price - float(price_tick_size)

    stop_price = get_price_with_precision(stop_price, price_tick_size)
    stop_limit_price = get_price_with_precision(stop_limit_price, price_tick_size)

    return stop_price, stop_limit_price


def get_price_with_precision(current_price, price_precision):
    price = round_step_size(float(current_price), float(price_precision))
    # Find the decimal place to format
    price_precision = str(price_precision)[::-1].find('.')
    price = "{:.{}f}".format(price, price_precision)
    return price


@lru_cache(maxsize=None)
def get_sym_filters(symbol):
    pair_info = client.get_symbol_info(symbol)
    if pair_info is not None:
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
    return None


def calculate_quantity(balance, current_price, precision):
    quantity = float(balance) / float(current_price)
    quantity = quantity - float(precision)
    target_quantity = round_step_size(quantity, float(precision))
    return float(target_quantity)


def get_asset_balance(asset_name=''):
    balance_symbol = 'BUSD'
    if asset_name:
        balance_symbol = asset_name
    balance_resp = client.get_asset_balance(balance_symbol)
    balance = 0
    if balance_resp['asset'] == balance_symbol:
        balance = balance_resp['free']
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
        logger.error(f'{side} with {symbol} quantity {quantity}: ' + e.message)
    else:
        return order_send


def place_stop_loss_order(symbol, quantity, stop_price, price):
    try:
        recv_window = 50000
        sl = client.create_order(symbol=symbol,
                                 side=SIDE_SELL,
                                 quantity=quantity,
                                 type=ORDER_TYPE_STOP_LOSS_LIMIT,
                                 timeInForce=TIME_IN_FORCE_GTC,
                                 price=price,
                                 stopPrice=stop_price,
                                 recvWindow=recv_window)

    except BinanceAPIException as e:
        logger.error(f'SL with {symbol} quantity {quantity}: ' + e.message)
    else:
        return sl


def my_round_step_size(quantity: Union[float, Decimal], step_size: Union[float, Decimal]) -> Union[int, Decimal]:
    if step_size == 1.0:
        return math.floor(quantity)
    elif step_size < 1.0:
        return Decimal(f'{quantity}').quantize(Decimal(f'{step_size}'), rounding=ROUND_DOWN)


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


# prepare_order('LUNABUSD', 'buy')
# calculate_stop_loss_prices('LUNABUSD')

# test
# order_filled = is_order_filled('LUNABUSD', 458282764)
# print(order_filled)
# if order_filled is False:
#     print(cancel_order('LUNABUSD', 458246373))
