import unicorn_binance_websocket_api

ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(['trade', 'kline_15m'], ['btcusdt'], output="UnicornFy")

while True:
    oldest_data_from_stream_buffer = ubwa.pop_stream_data_from_stream_buffer()
    if oldest_data_from_stream_buffer:
        price = oldest_data_from_stream_buffer.get('price')
        if price is not None:
            print(f"Price = {price}")
        # print(oldest_data_from_stream_buffer)
