import pandas as pd

path = 'intersect.csv'

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
cl_arr = f"\n//CLOSE\ncl_arr{str(j)} = array.new_float(0)\n"
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
push_cl_array = '// CLOSE \n'
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

for x in range(read_csv.size):
    counter_str = str(i)
    if i < 10:
        counter_str = '0' + counter_str
    cnt_str = str(j) + counter_str
    # symbol string
    str_test += 's' + str(j) + counter_str + " = input.symbol('" + read_csv.values[x][0] \
                + "', group = 'Symbols', inline = '" + 's' + str(j) + counter_str + "')\n"


    # u symbol string
    u_array_str += 'u' + str(j) + \
                   counter_str + " = input.bool(true,  title = \"\", group = 'Symbols', inline = 's" + str(j) + \
                   counter_str + "')\n"
    # security calls
    # [cl01, rsi01, tsi01, adx01, rvol01, sup01] = request.security(s01, timeframe.period, screener_func())

    security_calls += f"[cl{cnt_str}, rsi{cnt_str}, tsi{cnt_str}, adx{cnt_str}, rvol{cnt_str}, sup{cnt_str}] = " \
                      f"request.security(s{cnt_str}, timeframe.period, screener_func())\n"
    # Add Symbols
    push_s_array += f"array.push(s_arr{str(j)}, only_symbol(s{cnt_str}))\n"
    # Flags
    push_u_array += f"array.push(u_arr{str(j)}, u{cnt_str})\n"
    # Close
    push_cl_array += f"array.push(cl_arr{str(j)}, cl{cnt_str})\n"
    # Rsi
    push_rsi_array += f"array.push(rsi_arr{str(j)}, rsi{cnt_str})\n"
    # Tsi
    push_tsi_array += f"array.push(tsi_arr{str(j)}, tsi{cnt_str})\n"
    # Adx
    push_adx_array += f"array.push(adx_arr{str(j)}, adx{cnt_str})\n"
    # Relative volume
    push_rvol_array += f"array.push(rvol_arr{str(j)}, rvol{cnt_str})\n"
    # Supertrend
    push_sup_array += f"array.push(sup_arr{str(j)}, sup{cnt_str})\n"

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
        str_test += f'\n// Part {str(j)}\n\n'
        u_array_str += f'\n// Part {str(j)}\n\n'
        security_calls += f'\n// Part {str(j)}\n\n'

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

# if_clause_str = ''
# for k in range(1, j+1):
#     if_clause_str += f"if array.get(u_arr{k}, i)\n\t"
#     if_clause_str += f"supptrend_value = array.get(sup_arr{k}, i)\n\t"
#     if_clause_str += f"tsi_value = array.get(tsi_arr{k}, i)\n\t"
#     if_clause_str += f"adx_value = array.get(adx_arr{k}, i)\n\t"
#     if_clause_str += f"rvol_value = array.get(rvol_arr{k}, i)\n\t"
#     if_clause_str += f"alertCondition = getAlertCondition(supptrend_value, tsi_value, adx_value, rvol_value)\n\t"
#     if_clause_str += f"if alertCondition\n\t\t"
#     if_clause_str += f"tv_price = array.get(cl_arr{k}, i)\n\t\t"
#     if_clause_str += f"symbol_name = array.get(s_arr{k}, i)\n\t\t"
#     if_clause_str += f"rsi_value = array.get(rsi_arr{k}, i)\n\t\t"
#     if_clause_str += f"alertstring = getAlertString(symbol_name, tv_price, rsi_value, tsi_value, adx_value, rvol_value)\n\t\t"
#     if_clause_str += f"alert(alertstring, alert.freq_once_per_bar)\n"

if_clause_str = ''
for k in range(1, j+1):
    if_clause_str += f"if array.get(u_arr{k}, i)\n\t"
    if_clause_str += f"alertCondition = getAlertCondition(array.get(sup_arr{k}, i), array.get(tsi_arr{k}, i), array.get(adx_arr{k}, i), array.get(rvol_arr{k}, i))\n\t"
    if_clause_str += f"if alertCondition\n\t\t"
    if_clause_str += f"alertstring = getAlertString(array.get(s_arr{k}, i), array.get(cl_arr{k}, i), array.get(rsi_arr{k}, i), array.get(tsi_arr{k}, i), array.get(adx_arr{k}, i), array.get(rvol_arr{k}, i))\n\t\t"
    if_clause_str += f"alert(alertstring, alert.freq_once_per_bar)\n"

print(if_clause_str)
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
