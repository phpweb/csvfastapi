from binance.streams import ThreadedWebsocketManager
import utils as utils
from config import get_settings
import bn_client_private as bn_private
from debug_log import logger
from binance.helpers import round_step_size
import bn_client_no_async as sell_order
import tr_sockets_prvt_with_pair as live_price

api_key = get_settings().api_key
api_secret = get_settings().api_secret

twm = ThreadedWebsocketManager(api_key, api_secret)
# start is required to initialise its internal loop
twm.start()


def prepare_sl_order(symbol, bought_price):
    stop_price, price, quantity = calculate_stop_loss_prices_and_quantity(symbol, bought_price)
    sl_order = bn_private.place_stop_loss_order(symbol, quantity, price, stop_price)
    if sl_order == 'Stop price would trigger immediately.':
        sell_order.prepare_order(symbol, 'sell')


def calculate_stop_loss_prices_and_quantity(symbol, bought_price, percent=0.003):
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

    # current_price = utils.get_current_price(symbol)
    current_price = bought_price
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


def handle_user_socket_message(msg):
    if msg['e'] == 'executionReport':
        symbol = msg['s']
        if msg['S'] == 'BUY' and msg['X'] == 'FILLED':
            bought_price = msg['p']
            prepare_sl_order(symbol, bought_price)
        # If SL has placed and new then start watching live price
        if msg['S'] == 'SELL' and msg['o'] == 'STOP_LOSS_LIMIT' and msg['X'] == 'NEW':
            sl_price = msg['p']
            sl_order_id = msg['i']
            # watch_if_current_price_ls_stop_loss_price(symbol, sl_price)
            if utils.write_sl_to_pickle_file(symbol, sl_price, sl_order_id):
                live_price.start_trade_socket(symbol)
        # Stop trade socket if SELL is filled
        if (msg['S'] == 'SELL' and msg['o'] == 'STOP_LOSS_LIMIT' and msg['X'] == 'FILLED') \
                or (msg['S'] == 'SELL' and msg['o'] == 'LIMIT' and msg['X'] == 'FILLED') or \
                (msg['S'] == 'SELL' and msg['o'] == 'STOP_LOSS_LIMIT' and msg['X'] == 'CANCELED'):
            live_price.stop_trade_socket(symbol)
        print('yes only BUSD')
        print(msg)


twm.start_user_socket(callback=handle_user_socket_message)
