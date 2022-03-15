import time
from binance.client import Client
from binance.enums import *
from binance.helpers import round_step_size
from config import get_settings
from debug_log import logger
import utils as utils
import bn_client_private as bn_private

api_key = get_settings().api_key
api_secret = get_settings().api_secret
client = Client(api_key, api_secret)


def prepare_order(symbol, side):
    sym_filters = utils.get_sym_filters(symbol)
    if sym_filters is None:
        print('There is no such a sym.')
        return {"error": "There is no such a sym."}
    min_quantity = sym_filters['min_quantity']
    min_notional = sym_filters['min_notional']
    quantity_step_size = sym_filters['quantity_step_size']
    price_tick_size = sym_filters['price_tick_size']
    current_price = utils.get_current_price(symbol)

    # current_price = 65.12232
    quantity = 0
    current_price_with_precision = 0
    order_side = ''
    if side == 'buy':
        asset_symbol = utils.extract_balance_symbol_from_pair(symbol)
        asset_balance = bn_private.get_asset_balance(asset_symbol)
        # print(f'asset balance = {asset_balance} min notional = {min_notional}')
        if float(asset_balance) < float(min_notional):
            logger.info(f'Min notional is too small by BUY! {symbol}')
            return {"info": f"Min notional is too small by BUY! {symbol}"}
        current_price_with_precision = utils.get_price_with_precision(current_price, price_tick_size)
        quantity = utils.calculate_quantity(asset_balance, current_price_with_precision, quantity_step_size)
        # print(f'quantity {quantity} min quantity {min_quantity}')
        if float(quantity) < float(min_quantity):
            logger.info(f'Minimum quantity is not enough by BUY! {symbol}')
            return {"info": f"Minimum quantity is not enough by BUY! {symbol}"}
        order_side = SIDE_BUY
    if side == 'sell':
        bn_private.get_sp_tp_order_and_cancel(symbol)
        ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
        symbol_balance = bn_private.get_asset_balance(ticker_symbol)
        symbol_balance = float(symbol_balance) - float(quantity_step_size)
        quantity = round_step_size(float(symbol_balance), float(quantity_step_size))
        if float(quantity) < float(min_quantity):
            logger.info(f'Minimum quantity is not enough by SELL! {symbol}')
            return {"info": f"Minimum quantity is not enough by SELL! {symbol}"}
        current_price_with_precision = utils.get_price_with_precision(current_price, price_tick_size)
        quantity = round_step_size(float(quantity), float(quantity_step_size))
        order_side = SIDE_SELL
    order_placed = bn_private.create_order(symbol, order_side, quantity, ORDER_TYPE_LIMIT, current_price_with_precision)
    if order_placed:
        if order_placed['status'] == 'FILLED':
            print(f'Order {order_side} {symbol} successful.')
            if side == 'buy':
                after_buy_actions(order_placed)
        if order_placed['status'] != 'FILLED':
            time.sleep(2)
            order_id = order_placed['orderId']
            order_status = bn_private.is_order_filled(symbol, order_id)
            if order_status is False:
                terminate_order = bn_private.cancel_order(symbol, order_id)
                if terminate_order:
                    prepare_order(symbol, side)
            if order_status is True:
                print(f'Order {order_side} {symbol} successful after second try.')
                if side == 'buy':
                    after_buy_actions(order_placed)


def after_buy_actions(order_placed):
    # Persist this info for sale later
    symbol = order_placed['symbol']
    bought_price = order_placed['price']
    utils.write_bought_price_to_pickle_file(symbol, bought_price)
    prepare_sl_order(symbol)


def prepare_sl_order(symbol):
    stop_price, price, quantity = calculate_stop_loss_prices_and_quantity(symbol)
    bn_private.place_stop_loss_order(symbol, quantity, stop_price, price)


def calculate_stop_loss_prices_and_quantity(symbol, percent=0.0007):
    # 0.01 means 1 percent
    # 0.005 means half of 1 percent
    # 0.0001 means 1 out of 1 percent
    sym_filters = utils.get_sym_filters(symbol)
    if sym_filters is None:
        print('There is no such a sym.')
        return {"error": "There is no such a sym."}
    min_quantity = sym_filters['min_quantity']
    quantity_step_size = sym_filters['quantity_step_size']
    price_tick_size = sym_filters['price_tick_size']
    ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
    symbol_balance = bn_private.get_asset_balance(ticker_symbol)
    if float(symbol_balance) < float(min_quantity):
        logger.info(f'Minimum quantity is not enough by STOP! {symbol}')
        return {"error": f"Minimum quantity is not enough by STOP! {symbol}"}
    symbol_balance = float(symbol_balance) - float(quantity_step_size)
    quantity = round_step_size(float(symbol_balance), float(quantity_step_size))

    current_price = utils.get_current_price(symbol)
    stop_loss_amount = float(current_price) * float(percent)
    stop_price = float(current_price) - stop_loss_amount
    stop_limit_price = stop_price - float(price_tick_size)
    stop_price = utils.get_price_with_precision(stop_price, price_tick_size)
    stop_limit_price = utils.get_price_with_precision(stop_limit_price, price_tick_size)

    return stop_price, stop_limit_price, quantity
