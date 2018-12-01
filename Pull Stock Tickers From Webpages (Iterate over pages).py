#these codes show how to get data from webpages, and iterate over pages, divs, tables
#due to iterate over 34 pages, the codes will be slower

import pandas as pd
import numpy as np
import bs4 as bs
import requests

pd.set_option('display.Width', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 20)

#set page iterable variable
i=1

#set empty list, to append all symbols in each page
st=[]

#iterate pages: since there are 34 webpages, from 1 to 34
for i in range(35)[1:]:
        #define the address
        address='https://money.cnn.com/data/markets/sandp/'+ '?page='+ str(i)
        #use requests to get the webpage, and parse the page using BeautifulSoup
        re=requests.get(address)
        soup=bs.BeautifulSoup(re.text, 'html.parser')
        #get the div based on 'class' and 'id'
        div=soup.find('div', {'class':'wsod_containerSpacing',
                              'id':'wsod_indexConstituents'})
        #define a list
        tr=[]
        #iterate the 'table' and 'tr' to find symbol
        for table in div.findAll('table'):
                for row in table.findAll('tr')[1:]:
                                symbol=row.findAll('td')[0].find('a').text
                                #append the symbol in one page
                                tr.append(symbol)
        i=+1
        #append all symbols in each page
        st.append(tr)
#due to the symbols in each page is one list, there are 34 lists. Change to one list
df=[x for row in st for x in row]
#change the list to DataFrame
df=pd.DataFrame(df)

