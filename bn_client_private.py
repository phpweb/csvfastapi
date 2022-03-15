from decimal import Decimal, ROUND_DOWN
import math
from typing import Union
from binance.client import Client
from binance.enums import *
from config import get_settings
from debug_log import logger
from binance.exceptions import BinanceAPIException
import utils as utils

api_key = get_settings().api_key
api_secret = get_settings().api_secret
client = Client(api_key, api_secret)


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
        canceled_order = client.cancel_order(symbol=symbol, orderId=order_id)
    except BinanceAPIException as e:
        logger.error(e)
        print(e)
    else:
        return canceled_order


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
        # Create pickle file to persist if there is a sl order.
        utils.write_sl_to_pickle_file(symbol, price)
        return sl


def get_sp_tp_order_and_cancel(symbol):
    """
    We need to check if sl_exists not to make extra api requests by sell action.
    """
    sl_exists = utils.check_if_sl_exists(symbol)
    if sl_exists:
        open_orders = client.get_open_orders(symbol=symbol)
        if len(open_orders) == 0:
            # If sl has been meanwhile used then remove pickle file.
            utils.remove_sl_pickle_file(symbol)
            logger.info(f'There is no open SL or TP orders for {symbol}')
            return {"info": f'There is no open SL or TP orders for {symbol}'}
        open_orders = [x for x in open_orders if x['symbol'] == symbol]
        order_id = open_orders[0]['orderId']
        cancel_order(symbol, order_id)
        # Remove pickle file after canceling sl_order
        utils.remove_sl_pickle_file(symbol)
        logger.info(f'SL or TP order for {symbol} has been canceled.')


def my_round_step_size(quantity: Union[float, Decimal], step_size: Union[float, Decimal]) -> Union[int, Decimal]:
    if step_size == 1.0:
        return math.floor(quantity)
    elif step_size < 1.0:
        return Decimal(f'{quantity}').quantize(Decimal(f'{step_size}'), rounding=ROUND_DOWN)



