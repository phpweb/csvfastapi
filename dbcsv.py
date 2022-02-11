import websocket
import json
import pandas as pd

path = '/Users/r.gezer/Documents/htdocs/python/fastapi/csv/all.csv'
stream = 'wss://stream.binance.com:9443/ws/!miniTicker@arr'


def on_message(ws, message):
    msg = json.loads(message)
    print(msg)
    symbol = [x for x in msg if x['s'].endswith('USDT')]
    frame = pd.DataFrame(symbol)[['E', 's', 'c']]
    frame.E = pd.to_datetime(frame.E, unit='ms')
    frame.c = frame.c.astype(float)
    symbols = []
    for row in range(len(frame)):
        data = frame[row:row + 1]
        print('bunlar ne')
        print(data['s'].values[0])
        
        # data[['E', 'c']].to_csv(path + data['s'].values[0], mode='a', header=False)
        # Old data
        data[['s']].to_csv(path, mode='a', header=False, index=False)


ws = websocket.WebSocketApp(stream, on_message=on_message)
ws.run_forever()
