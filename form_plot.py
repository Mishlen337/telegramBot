import plotly.express as px

from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override()
from datetime import date, timedelta, datetime

from dateutil.relativedelta import relativedelta

data = pdr.get_data_yahoo('AAPL', start = date.today() - relativedelta(years=1), end=date.today())
print(data)
df = px.data.stocks()
fig = px.line(data, x=data.index, y="High")
fig.show()
