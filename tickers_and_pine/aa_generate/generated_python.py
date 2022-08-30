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
symbols_array = f'// SYMBOLS //\n// Part {str(j)}\n\n'
u_array_str = f'/////////////\n// SYMBOLS //\n// Part {str(j)}\n\n'
security_calls = f'// Security calls \n//Part {str(j)}\n\n'
# Add Symbols
push_s_array = '// Add Symbols \n'
# FLAGS
push_u_array = '// FLAGS \n'
# CLOSE
current_price_arr = '// Current price \n'
trend_arr = '// Super trend \n'
trend_minus_one_arr = '// Super trend minus one \n'
trendhtf_arr = '// trendhtf \n'
trendhtf_minus_one_arr = '// trendhtf minus one \n'

symbols_dict = {}
u_array_dict = {}
security_calls_dict = {}
push_s_array_dict = {}
push_u_array_dict = {}
push_cl_array_dict = {}
arrays_to_push_dict = {}
trend_dict = {}
trend_minus_one_dict = {}
trendhtf_dict = {}
trendhtf_minus_one_dict = {}

for x in range(read_csv.size):
    counter_str = str(i)
    if i < 10:
        counter_str = '0' + counter_str
    # cnt_str = str(j) + counter_str
    cnt_str = counter_str
    # symbol string
    symbols_array += 's' + cnt_str + " = input.symbol('" + read_csv.values[x][0] + "', group = 'Symbols', inline = '" + 's' + cnt_str + "')\n"
    symbols_dict[j] = symbols_array
    # u symbol string
    u_array_str += 'u' + cnt_str + " = input.bool(true,  title = '', group = 'Symbols', inline = 's" + cnt_str + "')\n"
    u_array_dict[j] = u_array_str
    # security calls
    security_calls += f"[current_price{cnt_str}, trend{cnt_str}, trend_minus_one{cnt_str}, trendhtf{cnt_str}, trendhtf_minus_one{cnt_str}] = request.security(s{cnt_str}, timeframe.period, screener_func())\n"
    security_calls_dict[j] = security_calls
    
    arrays_to_push1 = f'\n/////////////\n// ARRAYS //\n\n'
    arrays_to_push1 += f"s_arr   = array.new_string(0)\n"
    arrays_to_push2 = f"u_arr   = array.new_bool(0)\n"
    arrays_to_push3 = f"current_price_arr   = array.new_float(0)\n"
    arrays_to_push4 = "trend_arr = array.new_int(0) \n"
    arrays_to_push5 = "trend_minus_one_arr = array.new_int(0) \n"
    arrays_to_push6 = "trendhtf_arr = array.new_int(0) \n"
    arrays_to_push7 = "trendhtf_minus_one_arr = array.new_int(0) \n"
    arrays_to_push_dict[j] = arrays_to_push1 + arrays_to_push2 + arrays_to_push3 + arrays_to_push4 + arrays_to_push5 + arrays_to_push6 + arrays_to_push7 
    # Add Symbols
    push_s_array += f"array.push(s_arr, only_symbol(s{cnt_str}))\n"
    push_s_array_dict[j] = push_s_array
    # Flags
    push_u_array += f"array.push(u_arr, u{cnt_str})\n"
    push_u_array_dict[j] = push_u_array
    # Close price (current price)
    current_price_arr += f"array.push(current_price_arr, current_price{cnt_str})\n"
    push_cl_array_dict[j] = current_price_arr
    
    trend_arr += f"array.push(trend_arr, trend{cnt_str})\n"
    trend_dict[j] = trend_arr

    trend_minus_one_arr += f"array.push(trend_minus_one_arr, trend_minus_one{cnt_str})\n"
    trend_minus_one_dict[j] = trend_minus_one_arr

    trendhtf_arr += f"array.push(trendhtf_arr, trendhtf{cnt_str})\n"
    trendhtf_dict[j] = trendhtf_arr

    trendhtf_minus_one_arr += f"array.push(trendhtf_minus_one_arr, trendhtf_minus_one{cnt_str})\n"
    trendhtf_minus_one_dict[j] = trendhtf_minus_one_arr


    if i % max_items == 0:
        j += 1
        i = 0
    i += 1
calculations = ''
with open('functions.txt') as f:
    calculations += f.read()

if_condition_text = ''
with open('if_conditions.txt') as f:
    if_condition_text += f.read()

for k in range(1, j + 1):
    # pine script
    pine_script = f'//@version=5\nindicator("Benimki Supertrend MTF Heikin Ashi Part_{str(k)}", overlay=true)\n\n'

    with open(f'output/pine_part_{k}.txt', 'w') as f:
        f.write(pine_script)
        f.write(calculations)
        f.write(u_array_dict[k])
        f.write(symbols_dict[k])
        f.write(security_calls_dict[k])
        f.write(arrays_to_push_dict[k])
        f.write(push_s_array_dict[k])
        f.write(push_u_array_dict[k])
        f.write(push_cl_array_dict[k])
        f.write(trend_dict[k])
        f.write(trend_minus_one_dict[k])
        f.write(trendhtf_dict[k])
        f.write(trendhtf_minus_one_dict[k])
        f.write(if_condition_text)