from email_transactions.send_email import send_email_background
from conditions.long.requirements import check_enter_condition


def check_notification(df, background_tasks):
    timeframe = df['timeframe'].values[0]
    symbol = df['symbol'].values[0]
    entry_done = False
    if check_enter_condition(symbol, timeframe):
        subject = str(timeframe) + ' minutes'
        email_message_dict = {'symbol': symbol, 'current_timeframe': timeframe}
        send_email_background(background_tasks, subject, 'phpwebentwickler@gmail.com', email_message_dict)
        entry_done = True
    return entry_done
