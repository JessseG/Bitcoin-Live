import numpy
import talib
from numpy import genfromtxt

my_data = genfromtxt('15minutes.csv', delimiter=',')

# print(my_data)

close = my_data[:,4]

# print(close)

# close = numpy.random.random(100)

# print(close)

# moving_avg = talib.SMA(close, timeperiod=9)

# print(moving_avg)

rsi = talib.RSI(close)

print(rsi)