import plotly.express as px
import plotly
from pandas_datareader import data as pdr

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