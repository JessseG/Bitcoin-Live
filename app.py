from flask import Flask, render_template, request, flash, redirect, jsonify, send_from_directory
from binance.client import Client
from binance.enums import *
import config, csv, math, os, json

app = Flask(__name__)
app.secret_key = b'jf8943jhgh5.k9ghn549g.0-4g-04.g-0.45grco-03er'

client = Client(config.API_KEY, config.API_SECRET)

btc_usdt_tickSize = None
btc_usdt_stepSize = None

btc_eur_tickSize = None
btc_eur_stepSize = None

btc_usdt_raw_price = None

btc_raw_balance = None
usdt_raw_balance = None
eur_raw_balance = None

btc_usdt_trade_balance = None

btc_usdt_fee = None
btc_eur_fee = None

current_symbol = "BTCUSDT"
automation_symbol = current_symbol

candles = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","1d","3d"]
periods = ["1MINUTE","3MINUTE","5MINUTE","15MINUTE","30MINUTE","1HOUR","2HOUR","4HOUR","6HOUR","8HOUR","1DAY","3DAY"]
timeframes = [
    "14 Jan, 2021",
    "9 Jan, 2021",
    "5 Jan, 2021",
    "1 Dec, 2020",
    "1 Jul, 2020",
    "1 Apr, 2020",
    "1 Aug, 2019",
    "1 Apr, 2019",
    "1 Jan, 2019",
    "1 Jun, 2018",
    "1 Jan, 2017",
    "1 Jan, 2017"
]

def selectCandle(size):
    for i in range(len(candles)):
        if candles[i] == size:
            period = periods[i]
            print(period)
            return period

def selectTimeframe(size):
    for i in range(len(timeframes)):
        if candles[i] == size:
            timeframe = timeframes[i]
            print(timeframe)
            return timeframe
    
def floatPrecision(f, n):
        n = int(math.log10(1 / float(n)))
        f = math.floor(float(f) * 10 ** n) / 10 **n
        f = "{:0.0{}f}".format(float(f), n)
        return str(int(f)) if int(n) == 0 else f

def calculateMaxBuy(price, tick_size, quoteAsset_balance, step_size):
    limitPrice = floatPrecision(price, tick_size)
    quantity = floatPrecision(quoteAsset_balance / float(limitPrice), step_size)
    return quantity

def calculateMaxSell(price, tick_size, baseAsset_balance, step_size):
    limitPrice = floatPrecision(price, tick_size)
    quantity = floatPrecision(baseAsset_balance / float(limitPrice), step_size)
    return quantity

def buyMarketOrder(symbol, quoteAssetQty):
    try:
        print(f"Sending Order:  Market Buy - {quoteAssetQty} {symbol}")
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quoteOrderQty=quoteAssetQty)
        print(order)
    
    except Exception as e:
        # flash(e.message, "error")
        print("Exception occurred - {}".format(e))
        return False

    return order

def sellMarketOrder(symbol, quantity):
    try:
        print(f"Sending Order:  Market Sell - {quantity} {symbol}")
        order = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity)
        print(order)
    
    except Exception as e:
        # flash(e.message, "error")
        print("Exception occurred - {}".format(e))
        return False

    return order


@app.route('/webhook', methods=['POST'])
def webhook():
    # print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Failed Authentication"
        }
    
    print(data['bar'])

    side = data['strategy']['order-action'].upper()
    symbol = data['ticker']

    fee = None
    maxAmount = None
    balance = None

     # Gets latest prices
    btc_usdt_market_price = list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price']
    btc_eur_market_price = list(filter(lambda x: x['symbol'] == 'BTCEUR', client.get_all_tickers()))[0]['price']

    # Formats latest prices
    btc_usdt_price = floatPrecision(btc_usdt_market_price, btc_usdt_tickSize)
    btc_eur_price = floatPrecision(btc_eur_market_price, btc_eur_tickSize)

    btc_usdt_trade_balance = floatPrecision(btc_raw_balance, btc_usdt_stepSize)

    if symbol == "BTCUSDT":
        fee = float(btc_usdt_fee['tradeFee'][0]['taker'])
        if side == "BUY":
            usdt_max_trade = float(floatPrecision((usdt_raw_balance - (usdt_raw_balance * fee)), btc_usdt_tickSize))
            buyMarketOrder(symbol, usdt_max_trade)
        elif side == "SELL":
            btc_max_trade = float(floatPrecision((btc_raw_balance - (btc_raw_balance * fee)), btc_usdt_stepSize))
            sellMarketOrder(symbol, btc_max_trade)

    elif symbol == "BTCEUR":
        fee = float(btc_eur_fee['tradeFee'][0]['taker'])
        if side == "BUY":
            usdt_balance = float(floatPrecision((eur_raw_balance - (eur_raw_balance * fee)), btc_usdt_tickSize))
            maxAmount = float(floatPrecision(btc_raw_balance - btc_raw_balance * fee, btc_usdt_stepSize))
        elif side == "SELL":
            maxAmount = "hello"


    order_response = order(side, symbol, 0.000801)

    if order_response:
        return {
            "code": "success",
            "message": "Order Executed"
        }
    else:
        print("Order FAILED")
        return {
            "code": "Error",
            "message": "Order FAILED"
        }

    print(order_response)


@app.route('/')
def index():

    # info = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)

    info = client.get_account()
    # print(info)

    # Lists display_balances with a relevant balance
    display_balances = list(filter(lambda f: float(f['free']) >= 0.0000001, info['balances']))
    for asset in display_balances:
        if asset['asset'] == "USDT" or asset['asset'] == "EUR":
            asset['free'] = floatPrecision(float(asset['free']), 0.01)

    # print(balances)
    # print(client)
    # btc_balance = balances[0]['free']
    # usdt_balance = balances[11]['free']
    # eur_balance = balances[197]['free']

    global btc_raw_balance
    btc_raw_balance = float(client.get_asset_balance(asset='BTC')['free'])

    global usdt_raw_balance
    usdt_raw_balance = float(client.get_asset_balance(asset='USDT')['free'])

    global eur_raw_balance
    eur_raw_balance = float(client.get_asset_balance(asset='EUR')['free'])

    # exchange_info = client.get_exchange_info()
    # symbol_info = exchange_info['symbols']

    symbols = ["BTCUSDT", "BTCEUR", "EURUSDT"]

    # Gets fees for different trades: BTCUSDT & BTCEUR
    global btc_usdt_fee, btc_eur_fee
    btc_usdt_fee = client.get_trade_fee(symbol='BTCUSDT')['tradeFee'][0]['taker']
    btc_eur_fee = client.get_trade_fee(symbol='BTCEUR')

    # Gets the trading symbol info
    btc_usdt_info = client.get_symbol_info('BTCUSDT')
    btc_eur_info = client.get_symbol_info('BTCEUR')

    # Gets USDT & EUR price tickSizes for Selling BTC for USDT & EUR
    global btc_usdt_tickSize, btc_eur_tickSize
    btc_usdt_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_usdt_info['filters']))[0]['tickSize'])
    btc_eur_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_eur_info['filters']))[0]['tickSize'])
    
    # Gets BTC quantity stepSizes for Buying BTC with USDT & EUR
    global btc_usdt_stepSize, btc_eur_stepSize
    btc_usdt_stepSize = list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_usdt_info['filters']))[0]['stepSize']
    btc_eur_stepSize = list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_eur_info['filters']))[0]['stepSize']

    # Gets latest prices
    global btc_usdt_raw_price
    btc_usdt_raw_price = list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price']
    btc_eur_raw_price = list(filter(lambda x: x['symbol'] == 'BTCEUR', client.get_all_tickers()))[0]['price']

    # Formats latest prices
    btc_usdt_price = floatPrecision(btc_usdt_raw_price, btc_usdt_tickSize)
    btc_eur_price = floatPrecision(btc_eur_raw_price, btc_eur_tickSize)


    global btc_usdt_trade_balance
    btc_usdt_trade_balance = floatPrecision(btc_raw_balance, btc_usdt_stepSize)
    usdt_btc_trade_balance = floatPrecision(usdt_raw_balance, btc_usdt_tickSize)
    btc_eur_trade_balance = floatPrecision(btc_raw_balance, btc_eur_stepSize)
    eur_btc_trade_balance = floatPrecision(eur_raw_balance, btc_eur_tickSize)
    
    return render_template('index.html',
        my_balances=display_balances,
        symbols=symbols,
        usdt_fee=btc_usdt_fee,
        eur_fee=btc_eur_fee,
        btc_balance=btc_raw_balance,
        usdt_balance=usdt_raw_balance,
        eur_balance=eur_raw_balance,
        btc_usdt_info=btc_usdt_info,
        btc_eur_info=btc_eur_info,
        btc_usdt_tickSize=btc_usdt_tickSize,
        btc_eur_tickSize=btc_eur_tickSize,
        btc_usdt_stepSize=btc_usdt_stepSize,
        btc_eur_stepSize=btc_eur_stepSize,
        btc_usdt_price=btc_usdt_price,
        btc_eur_price=btc_eur_price)

@app.route('/buy', methods=['POST'])
def buy():
    try:
        order = client.create_order(
            symbol=request.form['symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=request.form['buy-limit-quantity'],
            price=request.form['buy-limit-price'])
    
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    try:
        order = client.create_order(
            symbol=request.form['symbol'],
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=request.form['sell-limit-quantity'],
            price=request.form['sell-limit-price'])
    
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/settings')
def settings():
    return 'Settings'

@app.route('/default')
def default():
    candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "1 Apr, 2019")
    # candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_2HOUR, "1 Aug, 2019")
    # candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Dec, 2020")
    # candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jan, 2021")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3], 
            "close": data[4],
        }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)


@app.route('/generate_candles', methods=['POST'])
def generateCandles():

    symbol = request.form['tradeSymbol']
    size = request.form['candleSize']

    period = selectCandle(size)
    timeframe = selectTimeframe(size)
    interval = str(f"Client.KLINE_INTERVAL_{period}")
    interval.strip()

    print(symbol)
    print(f"Client.KLINE_INTERVAL_{period}")
    print(timeframe)
    candlesticks = client.get_historical_klines_generator(symbol, eval(interval), timeframe)

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3], 
            "close": data[4],
        }
        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)

from app import app
app.run(debug=False)
# @app.route('/1m_candles')
# def min1():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "14 Jan, 2021")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/3m_candles')
# def min3():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_3MINUTE, "9 Jan, 2021")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/5m_candles')
# def min5():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "5 Jan, 2021")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/15m_candles')
# def min15():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Dec, 2020")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/30m_candles')
# def min30():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 Jul, 2020")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/1h_candles')
# def hour1():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Apr, 2020")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/2h_candles')
# def hour2():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_2HOUR, "1 Aug, 2019")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/4h_candles')
# def hour4():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "1 Apr, 2019")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/6h_candles')
# def hour6():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_6HOUR, "1 Jan, 2019")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/8h_candles')
# def hour8():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_8HOUR, "1 Jun, 2018")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/1d_candles')
# def day1():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

# @app.route('/3d_candles')
# def day3():
#     candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_3DAY, "1 Jan, 2017")

#     processed_candlesticks = []

#     for data in candlesticks:
#         candlestick = {
#             "time": data[0] / 1000,
#             "open": data[1],
#             "high": data[2],
#             "low": data[3], 
#             "close": data[4],
#         }
#         processed_candlesticks.append(candlestick)

#     return jsonify(processed_candlesticks)

@app.route('/max_buy', methods=['POST'])
def maximizeBuy():
    limitPrice = request.form['buyPrice']
    maxBuyAmount = float(calculateMaxBuy(limitPrice, btc_usdt_tickSize, usdt_raw_balance, btc_usdt_stepSize))
    return jsonify({'maxBuy': maxBuyAmount})

@app.route('/max_sell', methods=['POST'])
def maximizeSell():
    limitPrice = request.form['sellPrice']
    # maxSellAmount = calculateMaxBuy(limitPrice, btc_usdt_tickSize, btc_raw_balance, btc_usdt_stepSize)
    maxSellAmount = float(floatPrecision(btc_raw_balance, btc_usdt_stepSize))
    return jsonify({'maxSell': maxSellAmount})
     

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')
