# -*- coding: utf-8 -*-
"""
Модуль для формирования графиков
"""
import plotly.express as px
from pandas_datareader import data as pdr
from db_query import companies
import yfinance as yf
yf.pdr_override()
from datetime import date
from dateutil.relativedelta import relativedelta
import config

# download dataframe using pandas_datareader
def get_week_plot(name: str, user_chat_id:int):
    """
    Аргументы:
            имя компании
            чат id пользователя
    Цель: Сформировать файл с графиком изменения котировок за неделю.
    """
    ticker = companies.get_company_ticker(name)
    data = pdr.get_data_yahoo(ticker, start = date.today() - relativedelta(days=7), end=date.today())
    fig = px.line(data, x=data.index, y="High")
    fig.write_image(f"{config.image_path}/{user_chat_id}.png")

def get_month_plot(name: str, user_chat_id:int):
    """
    Аргументы:
            имя компании
            чат id пользователя
    Цель: Сформировать файл с графиком изменения котировок за месяц.
    """
    ticker = companies.get_company_ticker(name)
    data = pdr.get_data_yahoo(ticker, start = date.today() - relativedelta(month=1), end=date.today())
    fig = px.line(data, x=data.index, y="High")
    fig.write_image(f"{config.image_path}/{user_chat_id}.png")

def get_year_plot(name: str, user_chat_id:int):
    """
    Аргументы:
            имя компании
            чат id пользователя
    Цель: Сформировать файл с графиком изменения котировок за месяц.
    """
    ticker = companies.get_company_ticker(name)
    data = pdr.get_data_yahoo(ticker, start = date.today() - relativedelta(years=1), end=date.today())
    fig = px.line(data, x=data.index, y="High")
    fig.write_image(f"{config.image_path}/{user_chat_id}.png")
