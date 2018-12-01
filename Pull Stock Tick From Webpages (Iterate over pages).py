import numpy as np
import pandas as pd
import datetime
import pandas_datareader.data as web
import bs4 as bs
import requests

pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',50)
pd.set_option('display.width',100)
pd.set_option('compute.use_numexpr', True)
pd.set_option('compute.use_bottleneck', True)


re=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup=bs.BeautifulSoup(re.text, 'lxml')
table=soup.find('table', {'class':'wikitable sortable'})

tickers=[]
industries=[]

for row in table.findAll('tr')[1:]:
    symbol=row.findAll('td')[0].text
    industry=row.findAll('td')[3].text
    tickers.append(symbol)
    industries.append(industry)

df=pd.Series(industries, index=tickers)
   
df.index.name='tickers'    


start=datetime.datetime(2018,10,1)
end=datetime.datetime.now()

all_data={ticker: web.get_data_yahoo(ticker, start, end)
      for ticker in tickers[:20]}

price=pd.DataFrame({ticker: data['Adj Close']
                    for ticker, data in all_data.items()})

price=price.T

price.insert(0, 'industries', price.index.map(df))

price.index.names=['ticker']
price.reset_index(inplace=True)
price.set_index(['ticker','industries'], inplace=True)
price=price.T
