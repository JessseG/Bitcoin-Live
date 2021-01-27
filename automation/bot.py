# import websocket, json, pprint, talib, numpy
# from binance.client import Client
# from binance.enums import *
# import config

# SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
# RSI_PERIOD = 14
# RSI_OVERBOUGHT = 70
# RSI_OVERSOLD = 30
# TRADE_SYMBOL = "ETHUSDT"
# TRADE_QUANTITY = 0.05

# closes = []
# in_position = False

# client = Client(config.API_KEY, config.API_SECRET)

# # @app.route('/buy', methods=['POST'])
# def order(side, symbol, quantity, order_type=ORDER_TYPE_LIMIT):
#     try:
#         print("Sending Order")
#         order = client.create_order(
#             symbol=symbol,
#             side=side,
#             type=order_type,
#             timeInForce=TIME_IN_FORCE_GTC,
#             quantity=quantity)
#         print(order)
    
#     except Exception as e:
#         # flash(e.message, "error")
#         return False

#     return True

# def on_open(ws):
#     print('opened connection')

# def on_close(ws):
#     print('closed connection')

# def on_message(ws, message):
    
#     global closes

#     print('received message')
#     print(message)
#     json_message = json.loads(message)
#     pprint.pprint(json_message)

#     # specifies candle features in json
#     candle = json_message['k']

#     # check if candle closed
#     candle_closed = candle['x']

#     # closing price
#     close = candle['c']

#     # saves final candle prices to list
#     if candle_closed:
#         print("candle closed at {}".format(close))
#         closes.append(float(close))
#         print("closes")
#         print(closes)

#         if len(closes) > RSI_PERIOD:
#             np_closes = numpy.array(closes)
#             rsi = talib.RSI(np_closes, RSI_PERIOD)
#             print("All RSI calculated so far")
#             print(rsi)
#             last_rsi = rsi[-1]
#             print("The current RSI is {}".format(last_rsi))
#             global in_position
#             if last_rsi > RSI_OVERBOUGHT:
#                 if in_position:
#                     print("SELL !!")
#                     order_success = order(SIDE_SELL, TRADE_SYMBOL, TRADE_QUANTITY)
#                     if order_success:
#                         in_position = False
#                 else:
#                     print("Already Sold")

#             if last_rsi < RSI_OVERSOLD:
#                 if in_position:
#                     print("Already Bought")
#                 else:
#                     print("BUY !!")
#                     order_success = order(SIDE_BUY, TRADE_SYMBOL, TRADE_QUANTITY)
#                     if order_success:
#                         in_position = True

# def on_error(ws, error):
#     print(error)

# websocket.enableTrace(True)
# ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
# ws.run_forever()

