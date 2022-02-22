import os
import time
import pandas as pd
from sqlalchemy import create_engine

db_path = os.path.realpath('') + '/PricesTest.db'
engine = create_engine('sqlite:///' + db_path, connect_args={"check_same_thread": False})
start = time.time()
df = pd.read_sql_table('BTCUSDT', engine)
print(df)
request_time = time.time() - start
print(f'time passed {request_time}')
