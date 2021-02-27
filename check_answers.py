import config
import time
import telebot
import finance
import stock_parse
class Answers:
    def __init__(self):
        #self.list_of_notifications = [0,0,0]
        self.existence_of_polling = 0
        #self.storage = finance.Storage()
        #self.storage.upload_storage()

    def theory_answer_investment(self):
        return 'Здесь будет информация про инвестирование'
        
    def theory_answer_trading(self):
        return 'Здесь будет информация про трейдинг'

    def quote_answer_ruble(self,company):
        val, currency = stock_parse.parse_by_stockname(company)
        val = float(val) * float(stock_parse.parse_currency(currency))
        return f'Компания: {company} стоит {val:.2f} RUB'
    
    def quote_answer_currency(self,company):
        val, currency = stock_parse.parse_by_stockname(company)
        return f'Компания: {company} стоит {val} {currency}'
        

    #@classmethod
    def notification_answer(self,company):
        val, currency = stock_parse.parse_by_stockname(company)
        return f'Компания: {company} стоит {val} {currency}'
    


