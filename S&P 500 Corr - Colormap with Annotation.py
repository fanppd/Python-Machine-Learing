import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pickle
import os
import pandas_datareader.data as web
import bs4 as bs
import requests


def get_tickers():
    address='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    re=requests.get(address)
    soup=bs.BeautifulSoup(re.text,'html.parser')
    table=soup.find('table',{'class':'wikitable sortable'})

    tickers=[]
    sectors=[]

    for row in table.findAll('tr')[1:]:
        ticker=row.findAll('td')[1].text
        sector=row.findAll('td')[3].text   
        tickers.append(ticker)
        sectors.append(sector)

    tickers=pd.Series(tickers)
    sectors=pd.Series(sectors)

    df=pd.concat([tickers,sectors],axis=1)
    df.columns=['ticker','sector']
    df.set_index('sector',inplace=True)    

    with open('s&p500ticker.pickle','wb') as f:
        pickle.dump(df,f)

##get_tickers()

def get_price():
    if not os.path.exists('stock'):
        os.makedirs('stock')
    with open ('s&p500ticker.pickle','rb') as f:
        ticklers=pickle.load(f)

    start=datetime(2018,1,1)
    end=datetime.now()

    for ticker in ticklers['ticker'][:10]:
        if not os.path.exists('stock/{}.csv'.format(ticker)):
            df=web.get_data_yahoo(ticker,start,end)
            df.to_csv('stock/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

##get_price()



def combine_df():
    with open ('s&p500ticker.pickle','rb') as f:
        tickers=pickle.load(f)

    main_df=pd.DataFrame()
    
    for count, ticker in enumerate(tickers['ticker'][:10]):
        df=pd.read_csv('stock/{}.csv'.format(ticker))
        df.set_index('Date',inplace=True)
        df.rename(columns={'Adj Close':ticker},inplace=True)
        df.drop(['Open','Close','Volume','High','Low'],axis=1,inplace=True)
        if main_df.empty:
            main_df=df
        else:
            main_df=main_df.join(df,how='outer')

    main_df.to_csv('s&p500_combine.csv')



def color_map():
    df=pd.read_csv('s&p500_combine.csv')
    corr=df.corr()

    fig=plt.figure()
    ax=fig.add_subplot(111)

    cax=ax.imshow(corr, cmap=plt.cm.RdYlGn)
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)
    ax.xaxis.tick_top()
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            text=ax.text(i,j, '%.2f' % corr.iloc[i,j],
                         ha='center', va='center',color='k')
    fig.colorbar(cax)
    cax.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

color_map()

