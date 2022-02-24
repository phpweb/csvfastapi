import pandas as pd
import websocket
import json
from sqlalchemy import create_engine

engine = create_engine('sqlite:///Alltickers.db', connect_args={"check_same_thread": False})

stream = "wss://stream.binance.com:9443/ws/!miniTicker@arr"


def on_message(ws, message):
    msg = json.loads(message)
    symbol = [x for x in msg if x['s'].endswith('USDT')]
    frame = pd.DataFrame(symbol)[['E', 's', 'c']]
    frame.E = pd.to_datetime(frame.E, unit='ms')
    frame.c = frame.c.astype(float)
    for row in range(len(frame)):
        data = frame[row:row + 1]
        data[['E', 'c']].to_sql(data['s'].values[0], engine, index=False, if_exists='append')


ws = websocket.WebSocketApp(stream, on_message=on_message)
ws.run_forever()
