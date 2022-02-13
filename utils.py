import requests


def get_current_price(symbol):
    url = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    data = url.json()
    return data['price']


def calculate_win_los_percent_with_decimal(start_price, end_price):
    price_diff = ((float(start_price) / float(end_price)) * 100.00) - 100.00
    return round(price_diff, 2)
