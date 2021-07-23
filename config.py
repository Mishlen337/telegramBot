# -*- coding: utf-8 -*-
"""
Модуль для установки значений настроек
"""
from enum import Enum, auto
token_test =""
token = ""
apikey = ""
db_file = "./databases/Users.db"
notification_db_path = "./databases/notification.sqlite"
image_path = "./images"
url_begining = 'https://finance.yahoo.com/quote/'

class States(Enum):
    """Класс - перечисление состояний"""
    S_START = 0 # Начало нового диалога
    S_SETTINGS =auto()
    S_PRIMARY = auto()
    S_THEORY = auto()
    S_QUOTE = auto()
    S_GRAPH = auto()
    S_NOTIFICATION = auto()
    S_INVESTMENT = auto()
    S_TRADING = auto()
    S_RUBLE = auto()
    S_CURRENCY = auto()
    S_COMPANIES = auto()
    S_GWEEK = auto()
    S_GMONTH = auto()
    S_GYEAR = auto()
    S_TIME_DAY = auto()
    S_TIME_2DAYS = auto()
    S_TIME_WEEK = auto()
    S_CHANGE_COMPANIES = auto()
    S_ADD_COMPANIES = auto()
    S_DELETE_COMPANIES = auto()
    S_DELETE_SELECTIVELY = auto()

class NotificationStates(Enum):
    """
    Класс - перечисление уведомлений
    """
    NS_NONE = 0
    NS_DAY = 1
    NS_2DAYS = 2
    NS_WEEK = 3
