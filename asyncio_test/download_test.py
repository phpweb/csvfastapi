import asyncio
from tqdm import tqdm
import aiohttp
import pandas as pd
import datetime as dt
import time
from binance.client import Client

client = Client()
coins = ('BTCUSDT', 'ETHUSDT')


def get_minute_data_bn(symbol, lookback):
    data = client.get_historical_klines(symbol, '1m', lookback + ' days ago UTC')
    frame = pd.DataFrame(data)
    frame = frame.iloc[:, :5]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    frame[['Time', 'Open', 'High', 'Low', 'Close']] = frame[['Time', 'Open', 'High', 'Low', 'Close']].astype('float')
    frame.Time = pd.to_datetime(frame.Time, unit='ms')
    return frame


# for coin in tqdm(coins):
#     get_minute_data_bn(coin, '30').to_pickle(coin + '.pkl')


async def download_pep(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            print(content)
            return content


# asyncio.run(download_pep("https://www.python.org/dev/peps/pep-8010/"))

async def download_k_lines(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            print(content)
            return content


async def main() -> None:
    tasks = []
    for coin in tqdm(coins):
        tasks.append(get_minute_data_bn(coin, '30').to_pickle(coin + '.pkl'))
        # tasks.append(download_pep(url))
    await asyncio.wait(tasks)


asyncio.run(main())
