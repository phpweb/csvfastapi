import pandas as pd

usdt = pd.read_csv("all_usdt.csv", header=None)
busd = pd.read_csv("all_busd.csv", header=None)
# busd = busd[~busd.str.replace('BUSD', '')]
busd = busd[0].str.replace('BUSD', '')
usdt = usdt[0].str.replace('USDT', '')
intersected_df = pd.merge(usdt, busd, how='left')
# compare = pd.compare(busd, usdt)
# compare = busd.compare(usdt)
# compare = pd.concat([usdt, busd]).drop_duplicates(keep=False)
# compare.to_csv("compared.csv")
print(busd)
# print(usdt)
# print(intersected_df)
# print(compare)
