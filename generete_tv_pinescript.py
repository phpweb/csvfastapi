import pandas as pd

path = 'intersect.csv'

read_csv = pd.read_csv(path, header=None)
total = len(read_csv)
max_items = 40
i = 1
lst = []
j = 1
n = 5
str_test = ''
# s01 = input.symbol('RAREUSDT', group = 'Symbols', inline = 's01')
for x in range(read_csv.size):
    i_str = str(i)
    if i < 10:
        i_str = '0' + i_str
    if i % max_items == 0:
        lst.append(i)
        # str_test += i_str + ', '
        i = 0
    # print(read_csv.values[x][0] + 'USDT')
    # lst.append(read_csv.values[x][0] + 'USDT')
    # str_test += 's' + i_str + ', '
    str_test += 's' + i_str + " = input.symbol('" + read_csv.values[x][0]\
                + 'USDT' + "', group = 'Symbols', inline = '" + 's' + i_str + "')\n"
    lst.append(i)
    i += 1

# print(len(lst))
# print(lst)
# print(t)
# print(read_csv.size)
print(str_test)
