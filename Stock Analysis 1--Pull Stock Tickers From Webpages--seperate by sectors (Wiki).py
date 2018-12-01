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

#pull data from webpages; get tickers
for row in table.findAll('tr')[1:]:
    symbol=row.findAll('td')[0].text
    industry=row.findAll('td')[3].text
    tickers.append(symbol)
    industries.append(industry)

df=pd.Series(tickers, index=industries)
#Check groups, it same as: df.index.value_counts()
df.groupby(level=0).count()

#adjust the group
df.rename({'Communication Services\n':'Communication Services'}, inplace=True)
#get companies' name for sector 'Energy'
df.groupby(level=0).get_group('Energy')


