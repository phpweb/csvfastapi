from binance.spot import Spot as Client

client = Client(show_limit_usage=True, show_header=True)
print(client.time())
