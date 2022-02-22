import os
import pandas as pd
from sqlalchemy import create_engine
from collections import Counter
import datetime as dt

db_path = os.path.realpath('') + '/TvSignals.db'
print(db_path)
engine = create_engine('sqlite:///' + db_path, connect_args={"check_same_thread": False})

df = pd.read_sql_table('tv_signals_all', engine)
# mode, most frequent value in a column
# print(df['symbol'].mode())
now = dt.datetime.utcnow()
print(f"Simdi ne = {now}")
before = now - dt.timedelta(minutes=60*6)
df = df[(df['date'] > before) & (df['rvol'] > 5) & (df['timeframe'] == 15)]

count = Counter(df['symbol'])
count.most_common(3)
print(count)
