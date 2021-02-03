import config, csv, json
from binance.client import Client 

client = Client(config.API_KEY, config.API_SECRET)

# prices = client.get_all_tickers()

# for price in prices:
#     print(price)

# candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE)

# csvfile = open('15minutes.csv', 'w', newline='')

# for candle in candles:
#     print(candle)
#     candlestick_Writer.writerow(candle)

# print(len(candles))


# ______________________________________________________________________________________________
# CSV out to file


# csvfile = open('15_min_2020.csv', 'w', newline='')
# candlestick_writer = csv.writer(csvfile, delimiter=',')

# candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Jan, 2020")


# for candlestick in candlesticks:
#     candlestick[0] = candlestick[0] / 1000
#     candlestick_writer.writerow(candlestick)

# csvfile.close()

# ______________________________________________________________________________________________
# JSON out to file


# candlesticks = client.get_historical_klines_generator("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "1 Apr, 2019")

# processed_candlesticks = []

# for data in candlesticks:
#     candlestick = {
#         "time": data[0] / 1000,
#         "open": data[1],
#         "high": data[2],
#         "low": data[3], 
#         "close": data[4],
#     }
#     processed_candlesticks.append(candlestick)


# with open('candleData.json', 'w') as outfile:
#     json.dump(processed_candlesticks, outfile)