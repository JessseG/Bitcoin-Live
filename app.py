from flask import Flask, render_template, request, flash, redirect, jsonify, send_from_directory
from binance.client import Client
from binance.enums import *
import config, csv, math, os, json

app = Flask(__name__)
app.secret_key = b'jf8943jhgh5.k9ghn549g.0-4g-04.g-0.45grco-03er'

client = Client(config.API_KEY, config.API_SECRET)

btc_usdt_tickSize = None
btc_eur_tickSize = None
eur_usdt_tickSize = None

btc_usdt_stepSize = None
btc_eur_stepSize = None
eur_usdt_stepSize = None

btc_usdt_raw_price = None

btc_raw_balance = None
usdt_raw_balance = None
eur_raw_balance = None

btc_usdt_trade_balance = None

btc_usdt_fee = None
btc_eur_fee = None
eur_usdt_fee = None

current_symbol = "BTCUSDT"
automation_symbol = current_symbol

candles = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","1d","3d"]
periods = ["1MINUTE","3MINUTE","5MINUTE","15MINUTE","30MINUTE","1HOUR","2HOUR","4HOUR","6HOUR","8HOUR","1DAY","3DAY"]
timeframes = [
    "28 Jan, 2021", #1m
    "22 Jan, 2021", #3m
    "10 Jan, 2021", #5m
    "28 Dec, 2020", #15m
    "Nov 10, 2020", #30m
    "1 Apr, 2020",  #1H
    "1 Aug, 2019",  #2H
    "1 Apr, 2019",  #4H
    "1 Jan, 2019",  #6H
    "1 Jun, 2018",  #8H
    "1 Jan, 2017",  #1D
    "1 Jan, 2017"   #3D
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

def buyLimitOrder(symbol, quantity, price):
    try:
        print(f"Sending Order:  Limit Buy - {quantity} {symbol}")
        order = client.order_limit_buy(
            symbol=symbol,
            quantity=quantity,
            price=price)
        print(order)
    
    except Exception as e:
        # flash(e.message, "error")
        print("Exception occurred - {}".format(e))
        return False

    return order

def sellLimitOrder(symbol, quantity, price):
    try:
        print(f"Sending Order:  Limit Buy - {quantity} {symbol}")
        order = client.order_limit_sell(
            symbol=symbol,
            quantity=quantity,
            price=price)
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

    order_type = data['strategy']['order-type']
    side = data['strategy']['order-action'].upper()
    order_price = data['strategy']['order-price']
    symbol = data['ticker']

    # fee = None
    maxAmount = None
    balance = None

     # Gets latest prices
    btc_eur_last_price = list(filter(lambda x: x['symbol'] == 'BTCEUR', client.get_all_tickers()))[0]['price']

    # btc_usdt_fee = client.get_trade_fee(symbol='BTCUSDT')['tradeFee'][0]['maker']
    btc_eur_fee = client.get_trade_fee(symbol='BTCEUR')['tradeFee'][0]['maker']



    # Formats latest prices
    # btc_usdt_price = floatPrecision(btc_usdt_market_price, btc_usdt_tickSize)
    # btc_eur_price = floatPrecision(btc_eur_market_price, btc_eur_tickSize)

    # btc_usdt_trade_balance = floatPrecision(btc_raw_balance, btc_usdt_stepSize)

    # usdt_raw_balance - (usdt_raw_balance * fee)

    # Gets the trading symbol info
    btc_usdt_info = client.get_symbol_info('BTCUSDT')
    btc_eur_info = client.get_symbol_info('BTCEUR')

    global btc_raw_balance

    if order_type == "limit":
        if symbol == "BTCUSDT":
            if side == "BUY":
                btc_usdt_last_price = float(list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price'])
                btc_usdt_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_usdt_info['filters']))[0]['tickSize'])
                btc_usdt_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_usdt_info['filters']))[0]['stepSize'])
                usdt_raw_balance = float(client.get_asset_balance(asset='USDT')['free'])
                price = btc_usdt_last_price - 5
                quantity = float(calculateMaxBuy(price, btc_usdt_tickSize, usdt_raw_balance, btc_usdt_stepSize))
                order_response = buyLimitOrder(symbol, quantity, price)

            elif side == "SELL":
                btc_usdt_last_price = float(list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price'])
                # btc_usdt_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_usdt_info['filters']))[0]['tickSize'])
                btc_usdt_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_usdt_info['filters']))[0]['stepSize'])
                btc_raw_balance = float(client.get_asset_balance(asset='BTC')['free'])
                price = btc_usdt_last_price + 5
                quantity = float(floatPrecision(btc_raw_balance, btc_usdt_stepSize))
                # quantity = float(calculateMaxSell(price, btc_usdt_tickSize, usdt_raw_balance, btc_usdt_stepSize))
                order_response = sellLimitOrder(symbol, quantity, price)
        
        elif symbol == "BTCEUR":
            if side == "BUY":
                btc_eur_last_price = float(list(filter(lambda x: x['symbol'] == 'BTCEUR', client.get_all_tickers()))[0]['price'])
                btc_eur_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_eur_info['filters']))[0]['tickSize'])
                btc_eur_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_eur_info['filters']))[0]['stepSize'])
                eur_raw_balance = float(client.get_asset_balance(asset='EUR')['free'])
                price = btc_eur_last_price - 5
                quantity = float(calculateMaxBuy(price, btc_eur_tickSize, eur_raw_balance, btc_eur_stepSize))
                order_response = buyLimitOrder(symbol, quantity, price)

            elif side == "SELL":
                btc_eur_last_price = float(list(filter(lambda x: x['symbol'] == 'BTCEUR', client.get_all_tickers()))[0]['price'])
                # btc_eur_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_eur_info['filters']))[0]['tickSize'])
                btc_eur_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_eur_info['filters']))[0]['stepSize'])
                btc_raw_balance = float(client.get_asset_balance(asset='BTC')['free'])
                price = btc_eur_last_price + 5
                quantity = float(floatPrecision(btc_raw_balance, btc_eur_stepSize))
                print(quantity)
                # quantity = float(calculateMaxSell(price, btc_eur_tickSize, eur_raw_balance, btc_eur_stepSize))
                order_response = sellLimitOrder(symbol, quantity, price)

    elif order_type == "market":
        if symbol == "BTCUSDT":
            fee = float(0.001)
            # print(trade_balance)
            # fee = float(btc_usdt_fee)
            # fee = float(btc_usdt_fee['tradeFee'][0]['maker'])
            if side == "BUY":
                # global usdt_raw_balance
                usdt_raw_balance = float(client.get_asset_balance(asset='USDT')['free'])
                usdt_buy_balance = usdt_raw_balance - (usdt_raw_balance * fee)
                # global btc_usdt_tickSize
                btc_usdt_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_usdt_info['filters']))[0]['tickSize'])
                print(usdt_buy_balance)
                print(btc_usdt_tickSize)
                usdt_max_trade = float(floatPrecision(usdt_buy_balance, btc_usdt_tickSize))
                order_response = buyMarketOrder(symbol, usdt_max_trade)
            elif side == "SELL":
                btc_raw_balance = float(client.get_asset_balance(asset='BTC')['free'])
                btc_sell_balance = btc_raw_balance - (btc_raw_balance * fee)
                # global btc_usdt_stepSize
                btc_usdt_stepSize = list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_usdt_info['filters']))[0]['stepSize']
                btc_max_trade = float(floatPrecision(btc_sell_balance, btc_usdt_stepSize))
                order_response = sellMarketOrder(symbol, btc_max_trade)

        elif symbol == "BTCEUR":
            fee = float(0.001)
            # fee = float(btc_eur_fee)
            # fee = float(btc_eur_fee['tradeFee'][0]['maker'])
            if side == "BUY":
                # global eur_raw_balance
                eur_raw_balance = float(client.get_asset_balance(asset='EUR')['free'])
                eur_buy_balance = eur_raw_balance - (eur_raw_balance * fee)
                # global btc_eur_tickSize
                btc_eur_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_eur_info['filters']))[0]['tickSize'])
                print(eur_buy_balance)
                print(btc_eur_tickSize)
                eur_max_trade = float(floatPrecision(eur_buy_balance, btc_eur_tickSize))
                order_response = buyMarketOrder(symbol, eur_max_trade)

            elif side == "SELL":
                btc_raw_balance = float(client.get_asset_balance(asset='BTC')['free'])
                btc_sell_balance = btc_raw_balance - (btc_raw_balance * fee)
                # global btc_eur_stepSize
                btc_eur_stepSize = list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_eur_info['filters']))[0]['stepSize']
                btc_max_trade = float(floatPrecision(btc_sell_balance, btc_eur_stepSize))
                order_response = sellMarketOrder(symbol, btc_max_trade)

    # order_response = order(side, symbol, 0.000801)

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
    #useful for old heroku links
    # return redirect('http://bitcoin-live.trade/', code=302)
    
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
    global btc_usdt_fee, btc_eur_fee, eur_usdt_fee
    btc_usdt_fee = client.get_trade_fee(symbol='BTCUSDT')['tradeFee'][0]['maker']
    btc_eur_fee = client.get_trade_fee(symbol='BTCEUR')['tradeFee'][0]['maker']
    eur_usdt_fee = client.get_trade_fee(symbol='EURUSDT')['tradeFee'][0]['maker']

    # Gets the trading symbol info
    btc_usdt_info = client.get_symbol_info('BTCUSDT')
    btc_eur_info = client.get_symbol_info('BTCEUR')
    eur_usdt_info = client.get_symbol_info('EURUSDT')

    # Gets USDT & EUR price tickSizes for Selling BTC for USDT & EUR
    global btc_usdt_tickSize
    global btc_eur_tickSize
    global eur_usdt_tickSize
    btc_usdt_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_usdt_info['filters']))[0]['tickSize'])
    btc_eur_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', btc_eur_info['filters']))[0]['tickSize'])
    eur_usdt_tickSize = float(list(filter(lambda f: f['filterType'] == 'PRICE_FILTER', eur_usdt_info['filters']))[0]['tickSize'])
    
    # Gets BTC quantity stepSizes for Buying BTC with USDT & EUR
    global btc_usdt_stepSize, btc_eur_stepSize, eur_usdt_stepSize
    btc_usdt_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_usdt_info['filters']))[0]['stepSize'])
    btc_eur_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', btc_eur_info['filters']))[0]['stepSize'])
    eur_usdt_stepSize = float(list(filter(lambda f: f['filterType'] == 'LOT_SIZE', eur_usdt_info['filters']))[0]['stepSize'])

    # Gets latest prices
    global btc_usdt_raw_price
    btc_usdt_raw_price = float(list(filter(lambda x: x['symbol'] == 'BTCUSDT', client.get_all_tickers()))[0]['price'])
    btc_eur_raw_price = float(list(filter(lambda x: x['symbol'] == 'BTCEUR', client.get_all_tickers()))[0]['price'])

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
    if request.form['passcode-buy'] != config.SUBMISSION_CODE:
        return {
            "code": "error",
            "message": "Failed Authentication"
        }
    try:
        # regular limit order
        order = client.create_order(
            symbol=request.form['buy-symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=request.form['buy-limit-quantity'],
            price=request.form['buy-limit-price'])
    
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell', methods=['POST'])
def sell():
    if request.form['passcode-sell'] != config.SUBMISSION_CODE:
        return {
            "code": "error",
            "message": "Failed Authentication"
        }
    try:
        # regular limit order
        order = client.create_order(
            symbol=request.form['sell-symbol'],
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

@app.route('/default', methods=['POST'])
def default():
    candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "1 Apr, 2019")

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

    symbol = request.form['tradeSymbol'].upper()
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


@app.route('/max_buy', methods=['POST'])
def maximizeBuy():
    symbol = request.form['buySymbol']
    limitPrice = request.form['buyPrice']

    if symbol == "BTCUSDT":
        if usdt_raw_balance < 10:
            return jsonify({'maxBuy': 0})
        maxBuyAmount = float(calculateMaxBuy(limitPrice, btc_usdt_tickSize, usdt_raw_balance, btc_usdt_stepSize))
        # maxBuyAmount = float(floatPrecision((btc_raw_balance - (btc_raw_balance * btc_usdt_fee)), btc_usdt_stepSize)) #no longer taker fee
    elif symbol == "BTCEUR":
        if eur_raw_balance < 10:
            return jsonify({'maxBuy': 0})
        maxBuyAmount = float(calculateMaxBuy(limitPrice, btc_eur_tickSize, eur_raw_balance, btc_eur_stepSize))
        # maxBuyAmount = float(floatPrecision((btc_raw_balance - (btc_raw_balance * btc_eur_fee)), btc_eur_stepSize)) #no longer taker fee
    elif symbol == "EURUSDT":
        if usdt_raw_balance < 10:
            return jsonify({'maxBuy': 0})
        maxBuyAmount = float(calculateMaxBuy(limitPrice, eur_usdt_tickSize, usdt_raw_balance, eur_usdt_stepSize))

    print(maxBuyAmount)
    # maxBuyAmount = float(calculateMaxBuy(limitPrice, btc_usdt_tickSize, usdt_raw_balance, btc_usdt_stepSize))
    return jsonify({'maxBuy': maxBuyAmount})

@app.route('/max_sell', methods=['POST'])
def maximizeSell():
    symbol = request.form['sellSymbol']
    limitPrice = request.form['sellPrice']

    # limit sell no fee is calculated ??

    if symbol == "BTCUSDT":
        maxSellAmount = float(floatPrecision(btc_raw_balance, btc_usdt_stepSize))
        # maxSellAmount = floatPrecision((btc_raw_balance - (btc_raw_balance * btc_usdt_fee)), btc_usdt_stepSize) #no longer taker fee
    elif symbol == "BTCEUR":
        maxSellAmount = float(floatPrecision(btc_raw_balance, btc_eur_stepSize))
        # maxSellAmount = floatPrecision((btc_raw_balance - (btc_raw_balance * btc_eur_fee)), btc_eur_stepSize) #no longer taker fee
    elif symbol == "EURUSDT":
        maxSellAmount = float(floatPrecision(eur_raw_balance, btc_eur_stepSize))

    print(maxSellAmount)
    return jsonify({'maxSell': maxSellAmount})
     
@app.route('/max_autotrade', methods=['POST'])
def maximizeAutotrade():
    symbol = request.form['autoSymbol']

    # limit sell no fee is calculated ???

    if symbol == "BTCUSDT":
        maxAutoAmount = float(floatPrecision(btc_raw_balance, btc_usdt_stepSize))
        # maxSellAmount = floatPrecision((btc_raw_balance - (btc_raw_balance * btc_usdt_fee)), btc_usdt_stepSize) #no longer taker fee
    elif symbol == "BTCEUR":
        maxAutoAmount = float(floatPrecision(btc_raw_balance, btc_eur_stepSize))
        # maxSellAmount = floatPrecision((btc_raw_balance - (btc_raw_balance * btc_eur_fee)), btc_eur_stepSize) #no longer taker fee
    elif symbol == "EURUSDT":
        maxAutoAmount = float(floatPrecision(eur_raw_balance, btc_eur_stepSize))

    print(maxAutoAmount)
    return jsonify({'maxAuto': maxAutoAmount})
     

@app.route('/trade_history', methods=['POST']) 
def orderHistory():
    symbol = request.form['symbol']
    # orders = client.get_all_orders(symbol='BTCEUR', limit=10)
    trades = client.get_my_trades(symbol='BTCEUR')
    # print(orders)
    # print(trades)
    return jsonify(trades)

@app.route('/open_orders', methods=['POST'])
def openOrders():
    orders = client.get_open_orders(symbol='BTCEUR')
    return jsonify(orders)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'bitcoin-blue.png', mimetype='image/png')
