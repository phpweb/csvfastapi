import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

root_path = os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 2)[0] + '/'
# path_parent = os.path.dirname(os.getcwd()) + '/'
db_path = root_path + 'TvSignals.db'
engine = create_engine('sqlite:///' + db_path, connect_args={"check_same_thread": False})


def check_enter_condition(symbol, timeframe):
    time_period = [15, 5, 3]
    time_period_length = len(time_period)
    if timeframe >= 15:
        qry = f"SELECT * FROM tv_signals_all WHERE symbol = '{symbol}' ORDER BY date DESC LIMIT {time_period_length}"
        records = pd.read_sql_query(qry, engine)
        time_frames_equal = []
        if len(records) == time_period_length:
            for i in range(0, time_period_length):
                if records.iloc[i]['timeframe'] == time_period[i] or \
                        records.iloc[i]['timeframe'] == timeframe or \
                        records.iloc[i]['timeframe'] == time_period[i - 1]:
                    time_frames_equal.append(True)
                else:
                    time_frames_equal.append(False)
        notification = np.all(np.diff(time_frames_equal) == 0)
        return notification


# check_enter_condition('AGLDUSDT', 15)

# def possible_signals(df, background_tasks):
#     signal_timeframe = df['timeframe'].values[0]
#     if signal_timeframe >= 3:
#         symbol = df['symbol'].values[0]
#         # Check existing last time frame in possible table.
#         # If the last one has the same timeframe value then do not save anything in table.
#         now = dt.datetime.utcnow()
#         before = now - dt.timedelta(minutes=60)
#         check_existing_timeframe = f"SELECT * FROM tv_signals_possible WHERE symbol =
#         '{symbol}' and timeframe = {signal_timeframe} and date >= '{before}' ORDER BY timeframe DESC LIMIT 1"
#         df_check_existing_timeframe = pd.read_sql_query(check_existing_timeframe, engine)
#         print('existing last time frame')
#         print(df_check_existing_timeframe)
#         if df_check_existing_timeframe.empty:
#             print('should be executed')
#             timeframe = 1
#             if signal_timeframe == 5:
#                 timeframe = 3
#             if signal_timeframe == 15:
#                 timeframe = 5
#
#             time_frame_1 = f"SELECT * FROM tv_signals_all WHERE symbol = '{symbol}'
#             and timeframe = {timeframe} and date >= '{before}' ORDER BY date DESC LIMIT 1"
#             df_possible = pd.read_sql_query(time_frame_1, engine)
#             possible_dfs = df
#             if len(df_possible):
#                 df_possible['date'] = pd.to_datetime(df_possible['date'])
#                 possible_dfs = pd.concat([df_possible, df], ignore_index=True, sort=False)
#             possible_dfs.to_sql("tv_signals_possible", engine, index=False, if_exists='append')
#             email_message_dict = {}
#             if signal_timeframe >= 5:
#                 email_message_dict['symbol'] = symbol
#                 email_message_dict['previous_timeframe'] = timeframe
#                 email_message_dict['current_timeframe'] = signal_timeframe
#                 print('Email send possible')
#                 subject = str(signal_timeframe) + ' minutes'
#                 send_email_background(background_tasks, subject, 'phpwebentwickler@gmail.com', email_message_dict)
