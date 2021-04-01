from enum import Enum, auto
token_test ="1401737274:AAEr9_QYkCH5sblgCyZR2LHTtmqImFICaSY"
token = "1695721418:AAGx9FR9ry-JML7-SelZt32QtgOS1LbAdYE"
apikey = "89e10c73fe9cded3764526c1566fe4cb"
db_file = "/home/user/IsakovBot/telegramBot/Users.db"
notification_db_path = "/home/user/IsakovBot/telegramBot/notification.sqlite"
image_path = "/home/user/IsakovBot/telegramBot/images"
url_begining = 'https://finance.yahoo.com/quote/'
class States(Enum):
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
    S_TIME = auto()
    S_CHANGE_COMPANIES = auto()
    S_ADD_COMPANIES = auto()
    S_DELETE_COMPANIES = auto()
    S_DELETE_SELECTIVELY = auto()

class NotificationStates(Enum):
    NS_NONE = 0
    NS_DAY = 1
    NS_2DAYS = 2
    NS_WEEK = 3
