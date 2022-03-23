from os.path import exists
import pickle
import bn_client_no_async as bn
import bn_client_private as bn_private
# import tr_sockets as soc
# import tr_sockets_prvt as soc_prv
import time
import utils as utils

# bn.prepare_order('LUNABUSD', 'buy')
# bn.prepare_order('BTCBUSD', 'buy')
# current_price = bn.get_current_price('BTCBUSD')
# current_price = '0.1120'
# print(f'current price = {current_price}')
# sl = read_from_pickle_file('BTCBUSD')
# if sl is not False and float(current_price) < float(sl):
#     bn.prepare_order('BTCBUSD', 'sell')

# bn.get_sp_tp_order_and_cancel('DOGEBUSD')
# bn.calculate_stop_loss_prices('LUNABUSD')
# start = time.time()
# prepare_order('LUNABUSD', 'buy')
# request_time = time.time() - start
# print(f'NO asyncio time spent = {request_time}')

# start = time.time()
# bn.write_sl_to_pickle_file('DOGEBUSD', 0.765)
# sl_exists = bn.check_if_sl_exists('DOGEBUSD')
# # bn.remove_pickle_file('DOGEBUSD')
# request_time = time.time() - start
# print(f'NO asyncio sl exists = {sl_exists} time spent = {request_time}')

# soc.start_trade_socket('LUNABUSD')
# time.sleep(3)
# soc.start_socket('BTCUSDT')
# time.sleep(3)
# soc.stop_socket('LUNABUSD')

# percent = utils.calculate_win_los_percent(0.1450, 0.1453)
# print(f'percent = {percent}')

# bought_price = read_bought_price_from_pickle_file('LUNABUSD')
# print(f'Bought price from pickle file = {bought_price}')
# cancel_order_test = bn_private.cancel_order('LUNABUSD', 123232)
# print(cancel_order_test)
# if cancel_order_test == 'Unknown order sent.':
#     print('yesss')
# is_order_f = bn_private.is_order_filled('LUNABUSD', 123232)
# print(is_order_f)
# soc_prv.start_user_socket()
bn.prepare_order('DOGEBUSD', 'buy')
