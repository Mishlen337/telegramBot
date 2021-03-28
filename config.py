from enum import Enum, auto
token ="1401737274:AAEr9_QYkCH5sblgCyZR2LHTtmqImFICaSY"
apikey = "89e10c73fe9cded3764526c1566fe4cb"
db_file = "/Users/mikhailisakov/telegramBot/Users.db"
url_begining = 'https://finance.yahoo.com/quote/'
class States(Enum):
    S_START = 0 # Начало нового диалога
    S_PRIMARY = auto()
    S_THEORY = auto()
    S_QUOTE = auto()
    S_GRAPH = auto()
    S_NOTIFICATION = auto()
    S_INVESTMENT = auto()
    S_TRADING = auto()
    S_RUBLE = auto()
    S_CURRENCY = auto()
    S_DAY = auto()
    S_2DAYS = auto()
    S_WEEK = auto()
    S_GWEEK = auto()
    S_GMONTH = auto()
    S_GYEAR = auto()