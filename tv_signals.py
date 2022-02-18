import datetime as dt
from fastapi import FastAPI, BackgroundTasks, Request
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///TvSignals.db', connect_args={"check_same_thread": False})

app = FastAPI()


@app.post("/tv_signals")
async def root(request: Request):
    json_data = await request.json()
    df = pd.DataFrame([json_data])
    df['date'] = dt.datetime.utcnow()
    df.to_sql("tv_signals", engine, index=False, if_exists='append')
    print('dataframe')
    print(df)
    return {"json_data": json_data, "saved_db": True}
