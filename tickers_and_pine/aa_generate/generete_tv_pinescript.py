import os

# how many conditions, excepts close (price)
indicator_name = 'Benimki Bottom'
conditions = {
    'bottom': '// Bottom \\n',
    'data': '// Data \\n',
    'bought_price': '// bought_price \\n'
}

conditions_type = {
    'bottom': 'array.new_int(0) \\n',
    'data': 'array.new_bool(0) \\n',
    'bought_price': 'array.new_float(0) \\n'
}

directory = indicator_name.replace(' ', '_').lower()
if not os.path.isdir(directory):
    os.mkdir(directory)
# output directory
output_directory = directory + '/output'
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)
func_txt = directory + '/functions.txt'
if not os.path.exists(func_txt):
    os.close(os.open(func_txt, os.O_CREAT))
cond_txt = directory + '/conditions.txt'
if not os.path.exists(cond_txt):
    os.close(os.open(cond_txt, os.O_CREAT))
sym_txt = directory + '/all_usdt.csv'
if not os.path.exists(sym_txt):
    os.close(os.open(sym_txt, os.O_CREAT))


def generate_arrays():
    array_items = '\n'
    array_items_dict = '\n'
    security_calls = ''
    conditions_array_push = '\n'
    pushing_array_arrays = '\n'
    output_text = '\n'
    i = 4
    for key, value in conditions.items():
        array_items += f'{key}_arr = \'' + value + '\'\n'
        array_items_dict += f'{key}_dict = ' + '{}\n'
        security_calls += f', {key}' + '{cnt_str}'
        conditions_array_push += f'    arrays_to_push{i} = \"{key}_arr = ' + conditions_type[key] + '\"\n'
        pushing_array_arrays += f'    {key}_arr += f"array.push({key}_arr, {key}' + '{cnt_str}' + f')\\n"\n    {key}_dict[j] = {key}_arr\n\n'
        output_text += f'        f.write({key}_dict[k])\n'
        i += 1
    standard_array_items = '''
symbols_dict = {}
u_array_dict = {}
security_calls_dict = {}
push_s_array_dict = {}
push_u_array_dict = {}
push_cl_array_dict = {}
arrays_to_push_dict = {}'''
    if_condition_part_1 = '''
for x in range(read_csv.size):
    counter_str = str(i)
    if i < 10:
        counter_str = '0' + counter_str
    # cnt_str = str(j) + counter_str
    cnt_str = counter_str
    # symbol string
    symbols_array += 's' + cnt_str + " = input.symbol('" + read_csv.values[x][0] + "', group = 'Symbols', inline = '" + 's' + cnt_str + "')\\n"
    symbols_dict[j] = symbols_array
    # u symbol string
    u_array_str += 'u' + cnt_str + " = input.bool(true,  title = '', group = 'Symbols', inline = 's" + cnt_str + "')\\n"
    u_array_dict[j] = u_array_str
    # security calls
    security_calls += f"[current_price{cnt_str}{other_elements}] = request.security(s{cnt_str}, timeframe.period, screener_func())\\n"
    security_calls_dict[j] = security_calls
    '''.format(other_elements=security_calls, cnt_str='{cnt_str}')
    arrays_push_standard = '''
    arrays_to_push1 = f'\\n/////////////\\n// ARRAYS //\\n\\n'
    arrays_to_push1 += f"s_arr   = array.new_string(0)\\n"
    arrays_to_push2 = f"u_arr   = array.new_bool(0)\\n"
    arrays_to_push3 = f"current_price_arr   = array.new_float(0)\\n"'''
    all_arrays_push = '    arrays_to_push_dict[j] = '
    for i in range(1, len(conditions) + 4):
        all_arrays_push += f'arrays_to_push{i} + '
    all_arrays_push = all_arrays_push[:-2]

    push_arrays_standard = '''
    # Add Symbols
    push_s_array += f"array.push(s_arr, only_symbol(s{cnt_str}))\\n"
    push_s_array_dict[j] = push_s_array
    # Flags
    push_u_array += f"array.push(u_arr, u{cnt_str})\\n"
    push_u_array_dict[j] = push_u_array
    # Close price (current price)
    current_price_arr += f"array.push(current_price_arr, current_price{cnt_str})\\n"
    push_cl_array_dict[j] = current_price_arr
    '''
    some_if_condition = '''
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
    # pine script'''

    some_if_condition += '''
    pine_script = f'//@version=5\\nindicator("{script_name} Part_{strk}", overlay=true)\\n\\n'
'''.format(script_name=indicator_name, strk='{str(k)}')

    some_if_condition += '''
    with open(f'output/pine_part_{k}.txt', 'w') as f:
        f.write(pine_script)
        f.write(calculations)
        f.write(u_array_dict[k])
        f.write(symbols_dict[k])
        f.write(security_calls_dict[k])
        f.write(arrays_to_push_dict[k])
        f.write(push_s_array_dict[k])
        f.write(push_u_array_dict[k])
        f.write(push_cl_array_dict[k])'''

    output_text += '        f.write(if_condition_text)'

    headline_part = ''
    with open('head_part_1.txt') as f:
        headline_part += f.read()
    with open(f'{directory}/generated_python.py', 'w') as f:
        f.write(headline_part)
        f.write(array_items)
        f.write(standard_array_items)
        f.write(array_items_dict)
        f.write(if_condition_part_1)
        f.write(arrays_push_standard)
        f.write(conditions_array_push)
        f.write(all_arrays_push)
        f.write(push_arrays_standard)
        f.write(pushing_array_arrays)
        f.write(some_if_condition)
        f.write(output_text)
    print(headline_part)
    print(array_items)
    print(standard_array_items)
    print(array_items_dict)
    print(if_condition_part_1)
    print(arrays_push_standard)
    print(conditions_array_push)
    print(all_arrays_push)
    print(push_arrays_standard)
    print(pushing_array_arrays)
    print(some_if_condition)
    print(output_text)


generate_arrays()
