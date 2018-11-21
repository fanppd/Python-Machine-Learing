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

start=datetime.datetime(2018,1,1)
end=datetime.datetime.now()

data={symble: web.get_data_yahoo(symble, start, end)
    for symble in ['TSLA','AAPL']}


tsla=data['TSLA'][['Open', 'High','Low','Close']]
aapl=data['AAPL'][['Open', 'High','Low','Close']]

tsla.reset_index(inplace=True)
aapl.reset_index(inplace=True)

tsla['Date']=tsla['Date'].map(mdates.date2num)
aapl['Date']=aapl['Date'].map(mdates.date2num)

ax1=plt.subplot2grid((6,1),(0,0), rowspan=3, colspan=1)
ax2=plt.subplot2grid((6,1),(3,0), rowspan=3, colspan=1, sharex=ax1)


ax1.set_title('TSLA')
ax2.set_title('AAPL')

plt.setp(ax1.get_xticklabels(), visible=False)

ax1.xaxis_date()
ax2.xaxis_date()
ax1.plot(data['TSLA']['Close'].rolling(10, min_periods=0).mean(), label='10D')
ax2.plot(data['AAPL']['Close'].rolling(10, min_periods=0).mean(), label='10D')
candlestick_ohlc(ax1, tsla.values, colorup='g', width=0.5, alpha=0.5)
candlestick_ohlc(ax2, aapl.values, colorup='g', width=0.5, alpha=0.5)

ax1.legend(loc='best')
ax2.legend(loc='best')
plt.show()
