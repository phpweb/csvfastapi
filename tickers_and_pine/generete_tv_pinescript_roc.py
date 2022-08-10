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
rsi_arr = f"\n//RSI\nrsi_arr{str(j)} = array.new_float(0)\n"
tsi_arr = f"\n//TSI\ntsi_arr{str(j)} = array.new_float(0)\n"
adx_arr = f"\n//ADX\nadx_arr{str(j)} = array.new_float(0)\n"
rvol_arr = f"\n//RELATIVE VOLUME\nrvol_arr{str(j)} = array.new_float(0)\n"
sup_arr = f"\n//SUPERTREND\nsup_arr{str(j)} = array.new_float(0)\n"
# Add Symbols
push_s_array = '// Add Symbols \n'
# FLAGS
push_u_array = '// FLAGS \n'
# CLOSE
roc_array = '// ROC \n'
# RSI
push_rsi_array = '// RSI \n'
# TSI
push_tsi_array = '// TSI \n'
# ADX
push_adx_array = '// ADX \n'
# RELATIVE VOLUME
push_rvol_array = '// RELATIVE VOLUME \n'
# SUPERTREND
push_sup_array = '// SUPERTREND \n'

# arrays to create the type to push later
arrays_to_push = f'/////////////\n// ARRAYS //\n// Part {str(j)}\n\n'

str_test_dict = {}
u_array_dict = {}
security_calls_dict = {}
push_s_array_dict = {}
push_u_array_dict = {}
push_cl_array_dict = {}
arrays_to_push_dict = {}


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

    security_calls += f"roc{cnt_str} = request.security(s{cnt_str}, timeframe.period, screener_func())\n"

    security_calls_dict[j] = security_calls
    # crate arrays to push
    arrays_to_push1 = f'\n/////////////\n// ARRAYS //\n\n'
    arrays_to_push1 += f"s_arr   = array.new_string(0)\n"
    arrays_to_push2 = f"u_arr   = array.new_bool(0)\n"
    arrays_to_push3 = f"roc_arr   = array.new_float(0)\n"
    arrays_to_push_dict[j] = arrays_to_push1 + arrays_to_push2 + arrays_to_push3

    # Add Symbols
    push_s_array += f"array.push(s_arr, only_symbol(s{cnt_str}))\n"
    push_s_array_dict[j] = push_s_array
    # Flags
    push_u_array += f"array.push(u_arr, u{cnt_str})\n"
    push_u_array_dict[j] = push_u_array
    # Close
    roc_array += f"array.push(roc_arr, roc{cnt_str})\n"
    push_cl_array_dict[j] = roc_array
    # Rsi
    push_rsi_array += f"array.push(rsi_arr, rsi{cnt_str})\n"
    # Tsi
    push_tsi_array += f"array.push(tsi_arr, tsi{cnt_str})\n"
    # Adx
    push_adx_array += f"array.push(adx_arr, adx{cnt_str})\n"
    # Relative volume
    push_rvol_array += f"array.push(rvol_arr, rvol{cnt_str})\n"
    # Supertrend
    push_sup_array += f"array.push(sup_arr, sup{cnt_str})\n"

    if i % max_items == 0:
        j += 1
        # arrays
        s_array += f"s_arr{str(j)} = array.new_string(0)\n"
        u_arr += f"u_arr{str(j)} = array.new_bool(0)\n"
        cl_arr += f"cl_arr{str(j)} = array.new_float(0)\n"
        rsi_arr += f"rsi_arr{str(j)} = array.new_float(0)\n"
        tsi_arr += f"tsi_arr{str(j)} = array.new_float(0)\n"
        adx_arr += f"adx_arr{str(j)} = array.new_float(0)\n"
        rvol_arr += f"rvol_arr{str(j)} = array.new_float(0)\n"
        sup_arr += f"sup_arr{str(j)} = array.new_float(0)\n"
        # str_test += f'\n// Part {str(j)}\n\n'
        # make them empty after 40
        str_test = f'// SYMBOLS //\n// Part {str(j)}\n\n'
        u_array_str = f'/////////////\n// SYMBOLS //\n// Part {str(j)}\n\n'
        security_calls = f'// Security calls \n//Part {str(j)}\n\n'
        roc_array = '// ROC \n'
        push_s_array = '// Add Symbols \n'
        push_u_array = '// FLAGS \n'

        i = 0
    i += 1

if_condition_part1 = 'if barstate.islast'
# print(f'what is j = {j}')
if_condition_part1 += f"\n\tfor j = 1 to {j}"
if_condition_part1 += f"\n\t\tfor i = 1 to {max_items}"
if_condition_part1 += f"\n\t\t\tif array.get(u_arr + str.tostring(j), i)"
if_condition_part1 += f"\n\t\t\t\tsup_text = array.get(sup_arr + str.tostring(j), i) > 0 ? \"Down\" : \"Up\""
if_condition_part1 += f"\n\t\t\t\trvol_alert_condition = array.get(rvol_arr + str.tostring(j), i) > rvol_level ? true: false"
if_condition_part1 += f"\n\t\t\t\ttsi_alert_condition = array.get(tsi_arr + str.tostring(j), i) > 0 ? true : false"
if_condition_part1 += f"\n\t\t\t\tadx_alert_condition = array.get(adx_arr + str.tostring(j), i) > 20 ? true : false"
if_condition_part1 += f"\n\t\t\t\tsupertrend_alert_condition = sup_text == \"Up\" ? true : false"
if_condition_part1 += f"\n\t\t\t\tif rvol_alert_condition and supertrend_alert_condition"
# print(if_condition_part1)
# print(str_test)
# print(security_calls)
# print(u_arr)
# print(push_tsi_array)
# print(u_array_str)


if_clause_str = ''
for k in range(1, j+1):
    if_clause_str += f"if array.get(u_arr{k}, i)\n\t"
    if_clause_str += f"alertCondition = getAlertCondition(array.get(sup_arr{k}, i), array.get(tsi_arr{k}, i), array.get(adx_arr{k}, i), array.get(rvol_arr{k}, i))\n\t"
    if_clause_str += f"if alertCondition\n\t\t"
    if_clause_str += f"alertstring = getAlertString(array.get(s_arr{k}, i), array.get(cl_arr{k}, i), array.get(rsi_arr{k}, i), array.get(tsi_arr{k}, i), array.get(adx_arr{k}, i), array.get(rvol_arr{k}, i))\n\t\t"
    if_clause_str += f"alert(alertstring, alert.freq_once_per_bar)\n"

# print(f'J neci == {j}')
# print('u array ne')
# pprint.pprint(u_array_dict[1])
# with open('pine_part_uarray.txt', 'a') as f:
#     f.write(u_array_dict[1])
# u_array_dict = {}
# security_calls_dict = {}
# push_s_array_dict = {}
# push_u_array_dict = {}
# push_cl_array_dict = {}
calculations = '/////////////\n// CALCULATIONS //\n\n'
calculations += '// Get only symbol\n'
calculations += 'only_symbol(s) =>\n\tarray.get(str.split(s, ":"), 1)\n\n'
calculations += 'screener_func() =>\n\t//ROC\n\tpercent_change = ta.roc(close, 1)\n\tpercent_change\n\n'

# Alert condition
percentage_change_amount = 5
if_condition_part = 'if barstate.islast'
if_condition_part += f"\n\tfor i = 0 to array.size(u_arr) - 1"
if_condition_part += "\n\t\tif array.get(u_arr, i)"
if_condition_part += f"\n\t\t\troc_alert_condition = array.get(roc_arr, i) > {percentage_change_amount} ? true: false"
if_condition_part += "\n\t\t\tif roc_alert_condition"
if_condition_part += '\n\t\t\t\talertstring = \'{"symbol": "\' + array.get(s_arr, i) + \'"}\''
if_condition_part += '\n\t\t\t\talert(alertstring, alert.freq_once_per_bar)\n'
for k in range(1, j+1):
    # pine script
    pine_script = f'//@version=5\nindicator("Hourly 10% Part_{str(k)}", overlay=true)\n\n'
    with open(f'pine_part_{k}.txt', 'w') as f:
        f.write(pine_script)
        f.write(calculations)
        f.write(u_array_dict[k])
        f.write(str_test_dict[k])
        f.write(security_calls_dict[k])
        f.write(arrays_to_push_dict[k])
        f.write(push_s_array_dict[k])
        f.write(push_u_array_dict[k])
        f.write(push_cl_array_dict[k])
        f.write(if_condition_part)

# print(if_clause_str)
# with open('pine_part.txt', 'a') as f:
#     f.write(u_array_str)
#     f.write(str_test)
#     f.write(security_calls)
#     f.write(s_array)
#     f.write(u_arr)
#     f.write(cl_arr)
#     f.write(rsi_arr)
#     f.write(tsi_arr)
#     f.write(adx_arr)
#     f.write(rvol_arr)
#     f.write(sup_arr)
#     f.write(push_s_array)
#     f.write(push_u_array)
#     f.write(push_cl_array)
#     f.write(push_rsi_array)
#     f.write(push_tsi_array)
#     f.write(push_adx_array)
#     f.write(push_rvol_array)
#     f.write(push_sup_array)
