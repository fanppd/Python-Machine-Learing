import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader.data as web
from matplotlib import style
import pickle
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

##pd.set_option('display.max_rows',20)
##pd.set_option('display.max_columns',100)
##pd.set_option('display.width',100)
style.use('ggplot')


def get_data():
    start=datetime.datetime(1950,1,1)
    end=datetime.datetime.now()
    symble='^GSPC'   
    df=web.get_data_yahoo(symble,start,end)
    
    #create pickle
    with open('sp500_history.pickle','wb') as f:
        pickle.dump(df, f)


def calculate_plot():

    with open('sp500_history.pickle','rb') as f:
            df=pickle.load(f)

    price=df['Adj Close']

    #groupby 5 years' data
    grouped=price.groupby(pd.Grouper(freq='5Y', level='Date'))

    #only select tail of each group
    data=grouped.tail(1)

    #calculate percentage change
    pct=data.pct_change().dropna()


    fig, ax=plt.subplots()
    pct.plot.barh(ax=ax)
    #draw line on zero
    plt.axvline(0,color='k')

    ax.grid()
    ax.set_title("""S&P 500 from 1950 to 2018 - 5 years' Accumulated Return""")
    ax.set_yticklabels(pct.index.year)
    ax.set_xlabel('5 years accumulated return')
    ax.set_ylabel('Date (Year End)')

    #set xaxis as percentage format
    ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

    plt.show()

calculate_plot()
