from matplotlib import pyplot as plt
from yahoo_finance import Share
from pandas_datareader import data as pdr
import pandas

import yfinance as yf
yf.pdr_override()
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
#now = datetime.datetime.now()

# download dataframe using pandas_datareader

def stock_plot(x_axis, y_axis):
    fig, ax = plt.subplots()
    p = plt.plot(x_axis, y_axis)
    plt.ylabel('Value', color = 'gray')
    plt.xlabel('Date', color = 'gray')
    plt.xticks(rotation = 40)
    plt.yticks(rotation = 0.1)
    plt.grid(True)
    plt.savefig('foo.png', bbox_inches='tight')
    plt.close("all")

def get_plot(stockname: str, period: str):
    if period == "ГНеделя":
        data = pdr.get_data_yahoo(stockname, start = date.today() - relativedelta(days=7), end=date.today())
        dates = []
        quotes = []
        for index, row in data.iterrows():
            quotes.append(float(row.Close))

        for dat in list(data.index):
            dates.append(str(dat).split()[0])

        stock_plot(dates,quotes)

    if period == "ГМесяц":
        data = pdr.get_data_yahoo(stockname, start = date.today() - relativedelta(month=1), end=date.today())
        dates = []
        quotes = []
        for index, row in data.iterrows():
            quotes.append(float(row.Close))

        for dat in list(data.index):
            dates.append(str(dat).split()[0])

        stock_plot(dates,quotes)

    if period == "ГГод":
        data = pdr.get_data_yahoo(stockname, start = date.today() - relativedelta(years=7), end=date.today())
        dates = []
        quotes = []
        for index, row in data.iterrows():
            quotes.append(float(row.Close))

        for dat in list(data.index):
            dates.append(str(dat).split()[0])

        stock_plot(dates,quotes)
   

"""
def get_plot(stockname, callback):
    stock = Share(stockname)
    stock.get_historical()
    pass

stock = Share("TSLA")
print(stock.get_historical("24-07-2020", "25-07-2020"))
"""
#get_plot("AAPL").show()
#stock_plot(['1','2','3'],['s','sa','as']).show()