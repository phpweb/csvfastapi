import datetime as dt
from fastapi import FastAPI, BackgroundTasks, Request
import pandas as pd
from sqlalchemy import create_engine
from conditions import long
import bn_client_no_async as bn

engine = create_engine('sqlite:///TvSignals.db', connect_args={"check_same_thread": False})

app = FastAPI()


@app.get("/")
async def home():
    return {"it_is": "working."}


@app.post("/tv_signals")
async def root(request: Request, background_tasks: BackgroundTasks):
    json_data = await request.json()
    df = pd.DataFrame([json_data])
    df = df.astype({'rsi': 'float64', 'tsi': 'float64', 'adx': 'float64', 'rvol': 'float64', 'timeframe': 'int16'})
    df['date'] = dt.datetime.utcnow()
    entry = long.check_notification(df, background_tasks)
    df.to_sql("tv_signals_all", engine, index=False, if_exists='append')
    return {"json_data": json_data, "saved_db": True, "entry": entry}


@app.post("/luna")
async def luna(request: Request, background_tasks: BackgroundTasks):
    json_data = await request.json()
    df = pd.DataFrame([json_data])
    df['date'] = dt.datetime.utcnow()
    symbol = df['symbol'].values[0]
    side = df['side'].values[0]
    bn.prepare_order(symbol, side)
    df['position'] = 0
    df.to_sql("active_trades", engine, index=False, if_exists='append')
    return {"all": "is fine", "symbol": symbol}
