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
        if asset_balance < min_notional:
            logger.info(f'Min notional is too small by BUY! {symbol}')
            return {"info": f"Min notional is too small by BUY! {symbol}"}
        current_price_with_precision = utils.get_price_with_precision(current_price, price_tick_size)
        quantity = utils.calculate_quantity(asset_balance, current_price_with_precision, quantity_step_size)
        # print(f'quantity {quantity} min quantity {min_quantity}')
        if quantity < min_quantity:
            logger.info(f'Minimum quantity is not enough by BUY! {symbol}')
            return {"info": f"Minimum quantity is not enough by BUY! {symbol}"}
        order_side = SIDE_BUY
    if side == 'sell':
        bn_private.get_sp_tp_order_and_cancel(symbol)
        ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
        symbol_balance = bn_private.get_asset_balance(ticker_symbol)
        symbol_balance = symbol_balance - quantity_step_size
        quantity = round_step_size(symbol_balance, quantity_step_size)
        if quantity < min_quantity:
            logger.info(f'Minimum quantity is not enough by SELL! {symbol}')
            return {"info": f"Minimum quantity is not enough by SELL! {symbol}"}
        current_price_with_precision = utils.get_price_with_precision(current_price, price_tick_size)
        quantity = round_step_size(quantity, quantity_step_size)
        order_side = SIDE_SELL
    order_placed = bn_private.create_order(symbol, order_side, quantity, ORDER_TYPE_LIMIT, current_price_with_precision)
    if order_placed:
        if order_placed['status'] == 'FILLED':
            print(f'Order {order_side} {symbol} successful by first try.')
            logger.info(f'Order {order_side} {symbol} successful by first try.')
            if side == 'buy':
                after_buy_actions(order_placed)
        if order_placed['status'] != 'FILLED':
            time.sleep(2)
            order_id = order_placed['orderId']
            order_status = bn_private.is_order_filled(symbol, order_id)
            if order_status is False:
                terminate_order = bn_private.cancel_order(symbol, order_id)
                if terminate_order == 'Unknown order sent.' and side == 'buy':
                    # That means order has been already filled.
                    after_buy_actions(order_placed)
                    return True
                if terminate_order:
                    prepare_order(symbol, side)
            if order_status is True:
                print(f'Order {order_side} {symbol} successful after second try.')
                logger.info(f'Order {order_side} {symbol} successful after second try.')
                if side == 'buy':
                    after_buy_actions(order_placed)


def after_buy_actions(order_placed):
    # print('after buy actions')
    # Test
    # return True
    # Persist this info for sale later
    symbol = order_placed['symbol']
    bought_price = order_placed['price']
    utils.write_bought_price_to_pickle_file(symbol, bought_price)
    # prepare_sl_order(symbol)
    prepare_oco_order(symbol)


def prepare_sl_order(symbol):
    stop_price, price, quantity = calculate_stop_loss_prices_and_quantity(symbol)
    sl_order = bn_private.place_stop_loss_order(symbol, quantity, stop_price, price)
    if sl_order == 'Stop price would trigger immediately.':
        prepare_order(symbol, 'sell')


def calculate_stop_loss_prices_and_quantity(symbol, percent=0.005):
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
    if symbol_balance < min_quantity:
        logger.info(f'Minimum quantity is not enough by STOP! {symbol}')
        return {"error": f"Minimum quantity is not enough by STOP! {symbol}"}
    symbol_balance = symbol_balance - quantity_step_size
    quantity = round_step_size(symbol_balance, quantity_step_size)

    current_price = utils.get_current_price(symbol)
    stop_loss_amount = float(current_price) * percent
    stop_price = float(current_price) - stop_loss_amount
    stop_price = utils.get_price_with_precision(stop_price, price_tick_size)
    # With small amounts there can be situation that the stop price and current bought price is the same.
    if stop_price == current_price:
        stop_price = float(current_price) - float(price_tick_size)
    stop_limit_price = float(stop_price) - float(price_tick_size)
    stop_price = utils.get_price_with_precision(stop_price, price_tick_size)
    stop_limit_price = utils.get_price_with_precision(stop_limit_price, price_tick_size)

    return stop_limit_price, stop_price, quantity


def prepare_oco_order(symbol):
    stop_limit_price, stop_price, quantity = calculate_stop_loss_prices_and_quantity(symbol)
    tp_price = calculate_tp_price(symbol)
    print(f'stop_limit_price, stop_price, tp_price {stop_limit_price, stop_price, tp_price}')
    oco_order = bn_private.place_oco_order(symbol, quantity, stop_limit_price, stop_price, tp_price)
    if oco_order == 'Stop price would trigger immediately.':
        prepare_order(symbol, 'sell')


def calculate_tp_price(symbol, percent=0.01):
    sym_filters = utils.get_sym_filters(symbol)
    if sym_filters is None:
        print('There is no such a sym.')
        return {"error": "There is no such a sym."}
    min_quantity = sym_filters['min_quantity']
    price_tick_size = sym_filters['price_tick_size']
    ticker_symbol = utils.extract_ticker_symbol_from_pair(symbol)
    symbol_balance = bn_private.get_asset_balance(ticker_symbol)
    if symbol_balance < min_quantity:
        logger.info(f'Minimum quantity is not enough by STOP! {symbol}')
        return {"error": f"Minimum quantity is not enough by STOP! {symbol}"}
    current_price = utils.get_current_price(symbol)
    stop_loss_amount = float(current_price) * percent
    tp_price = float(current_price) + stop_loss_amount
    print(f'current price = {current_price}')
    print(f'price tick size = {price_tick_size}')
    tp_price = utils.get_price_with_precision(tp_price, price_tick_size)
    # If tp price is the same with the current price.
    if tp_price == current_price:
        tp_price = float(current_price) + (float(price_tick_size) + float(price_tick_size))
    tp_price = utils.get_price_with_precision(tp_price, price_tick_size)
    return tp_price
