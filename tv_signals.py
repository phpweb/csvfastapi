import datetime as dt
from fastapi import FastAPI, BackgroundTasks, Request
import pandas as pd
from sqlalchemy import create_engine
from email_transactions.send_email import send_email_background
from conditions import long

engine = create_engine('sqlite:///TvSignals.db', connect_args={"check_same_thread": False})

app = FastAPI()


@app.post("/tv_signals")
async def root(request: Request, background_tasks: BackgroundTasks):
    json_data = await request.json()
    df = pd.DataFrame([json_data])
    df = df.astype({'rsi': 'float64', 'tsi': 'float64', 'adx': 'float64', 'rvol': 'float64', 'timeframe': 'int16'})
    df['date'] = dt.datetime.utcnow()
    entry = long.check_notification(df, background_tasks)
    df.to_sql("tv_signals_all", engine, index=False, if_exists='append')
    return {"json_data": json_data, "saved_db": True, "entry": entry}
