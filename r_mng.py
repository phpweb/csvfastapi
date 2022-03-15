from os.path import exists
import pickle
import utils as utils
from debug_log import logger
import bn_client_private as bn_private
from binance.helpers import round_step_size


def update_stop_loss(symbol, percent=0.0007):
    """
    According to the timeframe calculate different percentages
    """
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
        logger.info(f'Minimum quantity is not enough by R_MNG! {symbol}')
        return {"error": f"Minimum quantity is not enough by R_MNG! {symbol}"}
    symbol_balance = float(symbol_balance) - float(quantity_step_size)
    quantity = round_step_size(float(symbol_balance), float(quantity_step_size))


last_sl_price = {
    'price': 0.0
}


def watch_sl_tp(msg):
    symbol = msg['s']
    bought_price = utils.read_bought_price_from_pickle_file(symbol)
    bought_price = 89.20
    if bought_price is not False:
        current_price = msg['p']
        print(f'Bought price from pickle file = {bought_price}')
        print(f"Current price: {current_price}")
        percent_win_or_lose = utils.calculate_win_los_percent(bought_price, current_price)
        if float(percent_win_or_lose) == 0.0002:
            last_sl_price['price'] = current_price
        print(f'percent_win_or_lose = {percent_win_or_lose}')
        print(f'last_sl_price = {last_sl_price}')
