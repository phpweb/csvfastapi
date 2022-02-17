import datetime as dt
import time
import os
import pandas as pd

from apscheduler.schedulers.background import BackgroundScheduler

from sqlalchemy import create_engine

engine = create_engine('sqlite:///Alltickers.db', connect_args={"check_same_thread": False})


def remove_old_records():
    symbols = pd.read_sql('SELECT name from sqlite_master WHERE type="table"', engine).name.to_list()
    now = dt.datetime.utcnow()
    before = now - dt.timedelta(minutes=10)
    for symbol in symbols:
        qry_str = f"""SELECT E,c FROM '{symbol}' WHERE E <= '{before}'"""
        df = pd.read_sql(qry_str, engine)
        if len(df) > 0:
            engine.execute(f"""DELETE FROM '{symbol}' WHERE E <= '{before}'""")
            print('deleted')


def tick():
    print('Tick! The time is: %s' % dt.datetime.now())


if __name__ == '__main__':
    scheduler = BackgroundScheduler(timezone="Europe/Berlin")
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.add_job(remove_old_records, 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
