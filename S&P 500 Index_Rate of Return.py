import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader.data as web
from matplotlib import style


##pd.set_option('display.max_rows',20)
##pd.set_option('display.max_columns',100)
##pd.set_option('display.width',100)


#setup the stype
style.use('ggplot')

#setup the start date and end date
start=datetime.datetime(2018,10,22)
end=datetime.datetime.now()

#setup ticker
symbol='^GSPC'

#pull data from yahoo finance
df=web.get_data_yahoo(symbol,start,end)

#caculate the percentage of return
pct_change=df['Adj Close'].pct_change().fillna(0).cumsum()

#pull example of top 10 rows
print(pct_change[:10])


#create fig
fig=plt.figure()

#setup the fig name
fig.canvas.set_window_title('S&P 500 Accumulated Return since ' +
                               str([start.year,start.month, start.day]) + ' to today')

#creat subplot
ax1=plt.subplot2grid((6,1),(0,0),rowspan=6,colspan=1)

#set title, ylabel, xlabel and legend
ax1.plot(pct_change, label='S&P 500')
ax1.set_title('S&P 500 Accumulated Return')
ax1.set_ylabel('Percentage of Return')
ax1.set_xlabel('Date')
ax1.legend(loc='best')

#run
plt.show()










