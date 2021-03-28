import config
import time
import telebot
import finance
import stock_parse

def theory_answer_investment():
    return 'Здесь будет информация про инвестирование'
        
def theory_answer_trading():
    return 'Здесь будет информация про трейдинг'

def quote_answer_ruble(company):
    val, currency = stock_parse.parse_by_stockname(company)
    val = float(val) * float(stock_parse.parse_currency(currency))
    return f'Компания: {company} стоит {val:.2f} RUB'
    
def quote_answer_currency(company):
    val, currency = stock_parse.parse_by_stockname(company)
    return f'Компания: {company} стоит {val} {currency}'
        

    #@classmethod
def notification_answer(self,company):
    val, currency = stock_parse.parse_by_stockname(company)
    return f'Компания: {company} стоит {val} {currency}'
    


