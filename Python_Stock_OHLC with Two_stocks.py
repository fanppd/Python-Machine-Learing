import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style
import datetime
import pandas_datareader.data as web
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

##pd.set_option('display.max_rows',50)
##pd.set_option('display.max_columns',200)
##pd.set_option('display.width',200)
##pd.set_option('compute.use_numexpr', True)
##pd.set_option('compute.use_bottleneck', True)
##pd.set_option('precision', 5)

#create start date and end date
start=datetime.datetime(2018,1,1)
end=datetime.datetime.now()

#pull data from yahoo
data={symble: web.get_data_yahoo(symble, start, end)
    for symble in ['TSLA','AAPL']}

#create OHLC
tsla=data['TSLA'][['Open', 'High','Low','Close']]
aapl=data['AAPL'][['Open', 'High','Low','Close']]

#reset index, inorder to create chart 
tsla.reset_index(inplace=True)
aapl.reset_index(inplace=True)

#set date as epoch time (matplotlib with candlestick_ohlc only accept epoch time)
tsla['Date']=tsla['Date'].map(mdates.date2num)
aapl['Date']=aapl['Date'].map(mdates.date2num)

#create subplot
ax1=plt.subplot2grid((6,1),(0,0), rowspan=3, colspan=1)
ax2=plt.subplot2grid((6,1),(3,0), rowspan=3, colspan=1, sharex=ax1)

#create title name
ax1.set_title('TSLA')
ax2.set_title('AAPL')

#delete ax1 x-axis label
plt.setp(ax1.get_xticklabels(), visible=False)

#set x-axis as date format
ax1.xaxis_date()
ax2.xaxis_date()

#create cummulate means
ax1.plot(data['TSLA']['Close'].rolling(10, min_periods=0).mean(), label='10D')
ax2.plot(data['AAPL']['Close'].rolling(10, min_periods=0).mean(), label='10D')

#create ohlc charts
candlestick_ohlc(ax1, tsla.values, colorup='g', width=0.5, alpha=0.5)
candlestick_ohlc(ax2, aapl.values, colorup='g', width=0.5, alpha=0.5)

#set legend location
ax1.legend(loc='best')
ax2.legend(loc='best')

#run plt
plt.show()
