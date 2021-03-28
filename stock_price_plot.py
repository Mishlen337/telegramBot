import plotly.express as px
import plotly
from pandas_datareader import data as pdr
from airium import Airium

import yfinance as yf
yf.pdr_override()
from datetime import date, timedelta, datetime

from dateutil.relativedelta import relativedelta
#now = datetime.datetime.now()

# download dataframe using pandas_datareader

def get_week_plot(stockname: str):
    data = pdr.get_data_yahoo(stockname, start = date.today() - relativedelta(days=7), end=date.today())
    fig = px.line(data, x=data.index, y="High")
    fig.write_image("plot.png")

def get_month_plot(stockname: str):
    data = pdr.get_data_yahoo(stockname, start = date.today() - relativedelta(month=1), end=date.today())
    fig = px.line(data, x=data.index, y="High")
    fig.write_image("plot.png")

def get_year_plot(stockname: str):    
    data = pdr.get_data_yahoo(stockname, start = date.today() - relativedelta(years=1), end=date.today())
    fig = px.line(data, x=data.index, y="High")
    fig.write_image("plot.png")
        #print(type(fig))
        #fig.show()
        #a = Airium()
        #a('<!DOCTYPE html>')
        #with a.html():
        #    with a.head():
        #        with a.html(lang='en'):
        #            a.meta(charset='utf-8')
        #            a.title(_t="Plot")
        #            a.link(href='style.css', rel='stylesheet', type='text/css')
        #            a.script(src='https://cdn.plot.ly/plotly-latest.min.js')
        #            a.font('Courier New, monospace')
                    #a.style()

        #    with a.body():
        #        a.append(plotly.offline.plot(fig, include_plotlyjs=False, output_type='div'))

        #html = str(a)
        #with open("./plot.html", 'w') as f:
        #    f.write(html)
"""
def get_plot(stockname, callback):
    stock = Share(stockname)
    stock.get_historical()
    pass

stock = Share("TSLA")
print(stock.get_historical("24-07-2020", "25-07-2020"))
"""
#stock_plot(['1','2','3'],['s','sa','as']).show()