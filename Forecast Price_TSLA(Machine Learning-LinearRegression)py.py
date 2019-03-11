import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader.data as web
from matplotlib import style
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

pd.set_option('display.Width',200)
pd.set_option('display.max_columns',200)
style.use('ggplot')

symbel='TSLA'
# pull data from yahoo finance
start=datetime.datetime(2010,1,1)
end=datetime.datetime(2019,2,26)
df=web.get_data_yahoo(symbel,start,end)
original=df.copy()
#create two variables
df['HL']=(df['High']-df['Low'])/df['Low']*100
df['OC']=(df['Open']-df['Close'])/df['Close']*100

#create X and y
df_test=df[['HL','OC','Volume','Close','Open','High','Low']]
    #shift up to 30 days
shift_up=30
forecast_test=df_test.iloc[-shift_up:]
df_test['Label']=df_test['Close'].shift(-shift_up)
    ##drop_value=df_test.copy()
df_test.dropna(inplace=True)

X=df_test.drop('Label',axis=1)
y=df_test['Label']

#machine training-LinearRegression
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.25)
clf=LinearRegression(n_jobs=-1)
clf.fit(X_train,y_train)
accuracy=clf.score(X_test,y_test)
forecast=clf.predict(forecast_test)

print(accuracy, forecast)

#merge the actual with prediction
forecast_test['Forecast']=np.nan
last_date=forecast_test.iloc[-1].name
last_date=datetime.datetime(year=last_date.year,month=last_date.month,day=last_date.day)
last_unix=last_date.timestamp()
one_day=86400
next_unix=last_unix+one_day
for i in forecast:
    next_date=datetime.datetime.fromtimestamp(next_unix)
    next_unix+=one_day
    forecast_test.loc[next_date]=[np.nan for _ in range(len(forecast_test.columns)-1)]+[i]

#plot charts
fig=plt.figure()
fig.canvas.set_window_title('Machine Learning(LinearRegression) for Stock Price Forecast')
    
forecast_test.loc['2018-1-1':,'Forecast'].plot()
plt.legend(loc=4)
plt.title(symbel + "'s price forecast for 30 days--from 2/28/2019")
plt.xlabel('Date')
plt.ylabel('Price')

#create chart for the actual values
start_actual=datetime.datetime(2018,1,1)
end_actual=datetime.datetime.now()
df_actual=web.get_data_yahoo(symbel,start_actual,end_actual)
df_actual['Adj Close'].plot(label='Actual')
plt.legend(loc='best')
plt.subplots_adjust(left=0.08,right=0.98,wspace=0.05,hspace=0.05)
plt.show()


