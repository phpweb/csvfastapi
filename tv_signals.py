import datetime as dt
from fastapi import FastAPI, BackgroundTasks, Request
import pandas as pd
from sqlalchemy import create_engine
from email_transactions.send_email import send_email_background

engine = create_engine('sqlite:///TvSignals.db', connect_args={"check_same_thread": False})

app = FastAPI()


@app.post("/tv_signals")
async def root(request: Request, background_tasks: BackgroundTasks):
    json_data = await request.json()
    df = pd.DataFrame([json_data])
    df = df.astype({'rsi': 'float64', 'tsi': 'float64', 'adx': 'float64', 'rvol': 'float64', 'timeframe': 'int16'})
    df['date'] = dt.datetime.utcnow()
    df.to_sql("tv_signals_all", engine, index=False, if_exists='append')
    possible_signals(df, background_tasks)
    # print('dataframe')
    # print(df)
    return {"json_data": json_data, "saved_db": True}


def possible_signals(df, background_tasks):
    signal_timeframe = df['timeframe'].values[0]
    if signal_timeframe >= 3:
        symbol = df['symbol'].values[0]
        # Check existing last time frame in possible table.
        # If the last one has the same timeframe value then do not save anything in table.
        now = dt.datetime.utcnow()
        before = now - dt.timedelta(minutes=60)
        check_existing_timeframe = f"SELECT * FROM tv_signals_possible WHERE symbol = '{symbol}' and timeframe = {signal_timeframe} and date >= '{before}' ORDER BY timeframe DESC LIMIT 1"
        df_check_existing_timeframe = pd.read_sql_query(check_existing_timeframe, engine)
        print('existing last time frame')
        print(df_check_existing_timeframe)
        if df_check_existing_timeframe.empty:
            print('should be executed')
            timeframe = 1
            if signal_timeframe == 5:
                timeframe = 3
            if signal_timeframe == 15:
                timeframe = 5

            time_frame_1 = f"SELECT * FROM tv_signals_all WHERE symbol = '{symbol}' and timeframe = {timeframe} and date >= '{before}' ORDER BY date DESC LIMIT 1"
            df_possible = pd.read_sql_query(time_frame_1, engine)
            possible_dfs = df
            if len(df_possible):
                df_possible['date'] = pd.to_datetime(df_possible['date'])
                possible_dfs = pd.concat([df_possible, df], ignore_index=True, sort=False)
            possible_dfs.to_sql("tv_signals_possible", engine, index=False, if_exists='append')
            email_message_dict = {}
            if signal_timeframe >= 5:
                email_message_dict['symbol'] = symbol
                email_message_dict['previous_timeframe'] = timeframe
                email_message_dict['current_timeframe'] = signal_timeframe
                print('Email send possible')
                subject = str(signal_timeframe) + ' minutes'
                send_email_background(background_tasks, subject, 'phpwebentwickler@gmail.com', email_message_dict)
