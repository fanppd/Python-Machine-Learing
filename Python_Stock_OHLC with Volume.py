import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas_datareader.data as web
from matplotlib import style

pd.set_option('display.max_rows',20)
pd.set_option('display.max_columns',100)
pd.set_option('display.width',100)
style.use('ggplot')

start=datetime.datetime(2017,1,1)
end=datetime.datetime.now()

symble='AMZN'

df=web.get_data_yahoo(symble,start,end)
print(df.columns)

data=df[['Open','High','Low','Close']]
data.reset_index(inplace=True)
data['Date']=data['Date'].map(mdates.date2num)


fig=plt.figure()
fig.canvas.set_window_title('Stock Price and Volume')


ax1=plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2=plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1,sharex=ax1)

ax1.xaxis_date()
ax2.xaxis_date()



candlestick_ohlc(ax1, data.values,colorup='g',width=0.5)
ax1.set_title(symble + '\'s stock price')
ax1.set_ylabel('Price')
ax1.plot(df['Adj Close'].rolling(30,min_periods=0).mean(), label='30D')
ax1.plot(df['Adj Close'].rolling(20,min_periods=0).mean(), label='20D')
ax1.plot(df['Adj Close'].rolling(10,min_periods=0).mean(), label='10D')
ax1.plot(df['Adj Close'].rolling(5,min_periods=0).mean(), label='5D')
ax1.legend(loc='best')

plt.setp(ax1.get_xticklabels(), visible=False)



ax2.fill_between(df.index.map(mdates.date2num),df['Volume'], color='g')
ax2.set_ylabel('Volume')
ax2.set_xlabel('Date')

print(data.head())

plt.show()
