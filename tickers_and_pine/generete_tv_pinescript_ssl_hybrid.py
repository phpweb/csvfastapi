import pandas as pd
import pprint

path = 'all_usdt.csv'

read_csv = pd.read_csv(path, header=None)
total = len(read_csv)
max_items = 40
i = 1
lst = []
j = 1
n = 5
str_test = f'// SYMBOLS //\n// Part {str(j)}\n\n'
u_array_str = f'/////////////\n// SYMBOLS //\n// Part {str(j)}\n\n'
security_calls = f'// Security calls \n//Part {str(j)}\n\n'
s_array = f"\n//ARRAYS\ns_arr{str(j)} = array.new_string(0)\n"
u_arr = f"\n//Symbols\nu_arr{str(j)} = array.new_bool(0)\n"
cl_arr = f"\n//ROC\roc_arr{str(j)} = array.new_float(0)\n"
current_price_arr = f"\n//CURRENT PRICE\ncurrent_price_arr{str(j)} = array.new_bool(0)\n"
buy_continuation_arr = f"\n//RSI\nbuy_continuation_arr{str(j)} = array.new_bool(0)\n"
baseLineBuyAlertCond_arr = f"\n//RSI\nbaseLineBuyAlertCond_arr{str(j)} = array.new_bool(0)\n"
baseLineSellAlertCond_arr = f"\n//RSI\nbaseLineSellAlertCond_arr{str(j)} = array.new_bool(0)\n"
codiff_plot_arr = f"\n//RSI\ncodiff_plot_arr_arr{str(j)} = array.new_bool(0)\n"
sslExitSell_arr = f"\n//TSI\nsslExitSell_arr{str(j)} = array.new_bool(0)\n"
sslExitBuy_arr = f"\n//TSI\nsslExitBuy_arr{str(j)} = array.new_bool(0)\n"
adx_arr = f"\n//ADX\nadx_arr{str(j)} = array.new_float(0)\n"
rvol_arr = f"\n//RELATIVE VOLUME\nrvol_arr{str(j)} = array.new_float(0)\n"
sup_arr = f"\n//SUPERTREND\nsup_arr{str(j)} = array.new_float(0)\n"
# Add Symbols
push_s_array = '// Add Symbols \n'
# FLAGS
push_u_array = '// FLAGS \n'
# CLOSE
current_price_arr = '// Current price \n'
buy_continuation_arr = '// Buy continuation \n'
baseLineBuyAlertCond_arr = '// Baseline BUY alert condition \n'
baseLineSellAlertCond_arr = '// Baseline SELL alert condition \n'
codiff_plot_arr = '// Condition for plotting \n'
sslExitSell_arr = '// SSL exit sell \n'
sslExitBuy_arr = '// SSL exit buy \n'

# arrays to create the type to push later
arrays_to_push = f'/////////////\n// ARRAYS //\n// Part {str(j)}\n\n'

str_test_dict = {}
u_array_dict = {}
security_calls_dict = {}
push_s_array_dict = {}
push_u_array_dict = {}
push_cl_array_dict = {}
arrays_to_push_dict = {}
buy_continuation_dict = {}
baseLineBuyAlertCond_dict = {}
baseLineSellAlertCond_dict = {}
codiff_plot_dict = {}
sslExitSell_dict = {}
sslExitBuy_dict = {}

for x in range(read_csv.size):
    counter_str = str(i)
    if i < 10:
        counter_str = '0' + counter_str
    # cnt_str = str(j) + counter_str
    cnt_str = counter_str
    # symbol string
    str_test += 's' + cnt_str + " = input.symbol('" + read_csv.values[x][0] \
                + "', group = 'Symbols', inline = '" + 's' + cnt_str + "')\n"
    str_test_dict[j] = str_test

    # u symbol string
    u_array_str += 'u' + cnt_str + " = input.bool(true,  title = \"\", group = 'Symbols', inline = 's" + cnt_str + "')\n"
    u_array_dict[j] = u_array_str
    # security calls
    # [cl01, rsi01, tsi01, adx01, rvol01, sup01] = request.security(s01, timeframe.period, screener_func())
    # if there are more than one function
    # security_calls += f"[cl{cnt_str}, rsi{cnt_str}, tsi{cnt_str}, adx{cnt_str}, rvol{cnt_str}, sup{cnt_str}] = " \
    #                   f"request.security(s{cnt_str}, timeframe.period, screener_func())\n"

    # security_calls += f"roc{cnt_str} = request.security(s{cnt_str}, timeframe.period, screener_func())\n"
    security_calls += f"[current_price{cnt_str}, buyContinuation{cnt_str}, baseLineBuyAlertCond{cnt_str}, baseLineSellAlertCond{cnt_str}, codiff_plot{cnt_str}, sslExitSell{cnt_str}, sslExitBuy{cnt_str}] = " \
                      f"request.security(s{cnt_str}, timeframe.period, screener_func())\n"

    security_calls_dict[j] = security_calls
    # crate arrays to push
    arrays_to_push1 = f'\n/////////////\n// ARRAYS //\n\n'
    arrays_to_push1 += f"s_arr   = array.new_string(0)\n"
    arrays_to_push2 = f"u_arr   = array.new_bool(0)\n"
    arrays_to_push3 = f"current_price_arr   = array.new_float(0)\n"
    arrays_to_push4 = f"buy_continuation_arr   = array.new_bool(0)\n"
    arrays_to_push5 = f"baseLineBuyAlertCond_arr   = array.new_bool(0)\n"
    arrays_to_push6 = f"baseLineSellAlertCond_arr   = array.new_bool(0)\n"
    arrays_to_push7 = f"codiff_plot_arr   = array.new_bool(0)\n"
    arrays_to_push8 = f"sslExitSell_arr   = array.new_bool(0)\n"
    arrays_to_push9 = f"sslExitBuy_arr   = array.new_bool(0)\n"
    arrays_to_push_dict[j] = arrays_to_push1 + arrays_to_push2 + arrays_to_push3 + arrays_to_push4 + arrays_to_push5 + arrays_to_push6 + arrays_to_push7 + arrays_to_push8 + arrays_to_push9

    # Add Symbols
    push_s_array += f"array.push(s_arr, only_symbol(s{cnt_str}))\n"
    push_s_array_dict[j] = push_s_array
    # Flags
    push_u_array += f"array.push(u_arr, u{cnt_str})\n"
    push_u_array_dict[j] = push_u_array
    # Close price (current price)
    current_price_arr += f"array.push(current_price_arr, current_price{cnt_str})\n"
    push_cl_array_dict[j] = current_price_arr
    # Buy continuation
    buy_continuation_arr += f"array.push(buy_continuation_arr, buyContinuation{cnt_str})\n"
    buy_continuation_dict[j] = buy_continuation_arr

    baseLineBuyAlertCond_arr += f"array.push(baseLineBuyAlertCond_arr, baseLineBuyAlertCond{cnt_str})\n"
    baseLineBuyAlertCond_dict[j] = baseLineBuyAlertCond_arr

    baseLineSellAlertCond_arr += f"array.push(baseLineSellAlertCond_arr, baseLineSellAlertCond{cnt_str})\n"
    baseLineSellAlertCond_dict[j] = baseLineSellAlertCond_arr

    codiff_plot_arr += f"array.push(codiff_plot_arr, codiff_plot{cnt_str})\n"
    codiff_plot_dict[j] = codiff_plot_arr

    sslExitSell_arr += f"array.push(sslExitSell_arr, sslExitSell{cnt_str})\n"
    sslExitSell_dict[j] = sslExitSell_arr

    sslExitBuy_arr += f"array.push(sslExitBuy_arr, sslExitBuy{cnt_str})\n"
    sslExitBuy_dict[j] = sslExitBuy_arr

    if i % max_items == 0:
        j += 1
        # arrays
        s_array += f"s_arr{str(j)} = array.new_string(0)\n"
        u_arr += f"u_arr{str(j)} = array.new_bool(0)\n"
        # str_test += f'\n// Part {str(j)}\n\n'
        # make them empty after 40
        str_test = f'// SYMBOLS //\n// Part {str(j)}\n\n'
        u_array_str = f'/////////////\n// SYMBOLS //\n// Part {str(j)}\n\n'
        security_calls = f'// Security calls \n//Part {str(j)}\n\n'
        roc_array = '// ROC \n'
        push_s_array = '// Add Symbols \n'
        push_u_array = '// FLAGS \n'
        current_price_arr = '// Current price \n'
        buy_continuation_arr = '// Buy continuation \n'
        baseLineBuyAlertCond_arr = '// Baseline BUY alert condition \n'
        baseLineSellAlertCond_arr = '// Baseline SELL alert condition \n'
        codiff_plot_arr = '// Condition for plotting \n'
        sslExitSell_arr = '// SSL exit sell \n'
        sslExitBuy_arr = '// SSL exit buy \n'

        i = 0
    i += 1


calculations = ''
with open('functions_ssl_hybrid.txt') as f:
    calculations += f.read()

if_condition_text = ''
with open('if_conditions_ssl_hybrid.txt') as f:
    if_condition_text += f.read()

for k in range(1, j + 1):
    # pine script
    pine_script = f'//@version=5\nindicator("SSL Hybrid Part_{str(k)}", overlay=true)\n\n'
    with open(f'ssl_hybrid/pine_part_{k}.txt', 'w') as f:
        f.write(pine_script)
        f.write(calculations)
        f.write(u_array_dict[k])
        f.write(str_test_dict[k])
        f.write(security_calls_dict[k])
        f.write(arrays_to_push_dict[k])
        f.write(push_s_array_dict[k])
        f.write(push_u_array_dict[k])
        f.write(push_cl_array_dict[k])
        f.write(buy_continuation_dict[k])
        f.write(baseLineBuyAlertCond_dict[k])
        f.write(baseLineSellAlertCond_dict[k])
        f.write(codiff_plot_dict[k])
        f.write(sslExitSell_dict[k])
        f.write(sslExitBuy_dict[k])
        # f.write(if_condition_part)
        f.write(if_condition_text)

