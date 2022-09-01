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
bottom_arr = '// Bottom \n'
data_arr = '// Data \n'
bought_price_arr = '// bought_price \n'

symbols_dict = {}
u_array_dict = {}
security_calls_dict = {}
push_s_array_dict = {}
push_u_array_dict = {}
push_cl_array_dict = {}
arrays_to_push_dict = {}
bottom_dict = {}
data_dict = {}
bought_price_dict = {}

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
    security_calls += f"[current_price{cnt_str}, bottom{cnt_str}, data{cnt_str}, bought_price{cnt_str}] = request.security(s{cnt_str}, timeframe.period, screener_func())\n"
    security_calls_dict[j] = security_calls
    
    arrays_to_push1 = f'\n/////////////\n// ARRAYS //\n\n'
    arrays_to_push1 += f"s_arr   = array.new_string(0)\n"
    arrays_to_push2 = f"u_arr   = array.new_bool(0)\n"
    arrays_to_push3 = f"current_price_arr   = array.new_float(0)\n"
    arrays_to_push4 = "bottom_arr = array.new_int(0) \n"
    arrays_to_push5 = "data_arr = array.new_bool(0) \n"
    arrays_to_push6 = "bought_price_arr = array.new_float(0) \n"
    arrays_to_push_dict[j] = arrays_to_push1 + arrays_to_push2 + arrays_to_push3 + arrays_to_push4 + arrays_to_push5 + arrays_to_push6 
    # Add Symbols
    push_s_array += f"array.push(s_arr, only_symbol(s{cnt_str}))\n"
    push_s_array_dict[j] = push_s_array
    # Flags
    push_u_array += f"array.push(u_arr, u{cnt_str})\n"
    push_u_array_dict[j] = push_u_array
    # Close price (current price)
    current_price_arr += f"array.push(current_price_arr, current_price{cnt_str})\n"
    push_cl_array_dict[j] = current_price_arr
    
    bottom_arr += f"array.push(bottom_arr, bottom{cnt_str})\n"
    bottom_dict[j] = bottom_arr

    data_arr += f"array.push(data_arr, data{cnt_str})\n"
    data_dict[j] = data_arr

    bought_price_arr += f"array.push(bought_price_arr, bought_price{cnt_str})\n"
    bought_price_dict[j] = bought_price_arr


    if i % max_items == 0:
        j += 1
        i = 0
    i += 1
calculations = ''
with open('functions.txt') as f:
    calculations += f.read()

if_condition_text = ''
with open('conditions.txt') as f:
    if_condition_text += f.read()

for k in range(1, j + 1):
    # pine script
    pine_script = f'//@version=5\nindicator("Benimki Bottom Part_{str(k)}", overlay=true)\n\n'

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
        f.write(bottom_dict[k])
        f.write(data_dict[k])
        f.write(bought_price_dict[k])
        f.write(if_condition_text)