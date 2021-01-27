wss://stream.binance.com:9443 // Binance base endpoint

wscat -c wss://stream.binance.com:9443/ws/btcusdt@trade // -c connect to Binance trade stream in real time

{  
 "e":"trade", // event type  
 "E":1609013645934,
"s":"BTCUSDT",
"t":527297557,
"p":"25857.63000000",
"q":"0.00208800",
"b":4034420785,
"a":4034423873,
"T":1609013645933, // unix time stamp
"m":true,
"M":true
}

wscat -c wss://stream.binance.com:9443/ws/btcusdt@kline_5m // -c connect to 5-minute candle sticks

{
"e":"kline",
"E":1609015000045,
"s":"BTCUSDT",
"k": {
"t":1609014900000,
"T":1609015199999,
"s":"BTCUSDT",
"i":"5m",
"f":527320601,
"L":527325287,
"o":"25994.13000000",
"c":"26034.09000000",
"h":"26040.00000000",
"l":"25970.64000000",
"v":"342.54938300",
"n":4687,
"x":false,
"q":"8908284.17312817",
"V":"247.67712400",
"Q":"6441074.79927864",
"B":"0"
}
}

wscat -c wss://stream.binance.com:9443/ws/btcusdt@kline_5m | tee Candles-5-min.json // connects to 5-min feed and saves to file
