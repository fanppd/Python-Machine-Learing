import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc


##pd.set_option('display.max_rows',50)
##pd.set_option('display.max_columns',200)
##pd.set_option('display.width',200)
##pd.set_option('compute.use_numexpr', True)
##pd.set_option('compute.use_bottleneck', True)
##pd.set_option('precision', 5)

#set start date and end date
start=datetime.datetime(2018,1,1)
end=datetime.datetime.now()

#pull data from yahoo_finance; 'data' is dict format, key would be symbols
data={symbol: web.get_data_yahoo(symbol, start, end)
    for symble in ['TSLA','AAPL']}

#set symble with associated data: OHLC
tsla=data['TSLA'][['Open', 'High','Low','Close']]
aapl=data['AAPL'][['Open', 'High','Low','Close']]

#reset index inorder to change datetime to epoch times(integer data)
tsla.reset_index(inplace=True)
aapl.reset_index(inplace=True)

#change datetime to epoch times(integer data); due to matplotlib.pyplot chart only accept epoch times
tsla['Date']=tsla['Date'].map(mdates.date2num)
aapl['Date']=aapl['Date'].map(mdates.date2num)

#create subplots
ax1=plt.subplot2grid((6,1),(0,0), rowspan=3, colspan=1)
ax2=plt.subplot2grid((6,1),(3,0), rowspan=3, colspan=1, sharex=ax1)

#create titles for each subplot
ax1.set_title('TSLA')
ax2.set_title('AAPL')

#delete ax1's labels(x-axis)
plt.setp(ax1.get_xticklabels(), visible=False)

#change the subplots' label (x-axis) to datetime
ax1.xaxis_date()
ax2.xaxis_date()

#create OHLC charts for ax1 and ax2
candlestick_ohlc(ax1, tsla.values, colorup='g', width=0.5, alpha=0.5)
candlestick_ohlc(ax2, aapl.values, colorup='g', width=0.5, alpha=0.5)

#create moving average: 10 days
ax1.plot(data['TSLA']['Close'].rolling(10, min_periods=0).mean(), label='10D')
ax2.plot(data['AAPL']['Close'].rolling(10, min_periods=0).mean(), label='10D')

#show up the label, location as best
ax1.legend(loc='best')
ax2.legend(loc='best')

#run the plt
plt.show()
