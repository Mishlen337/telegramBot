import config
import time
import telebot
import finance

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
        return 'Рубли'
    
    def quote_answer_currency(self,company):
        return 'Текущее'
        

    #@classmethod
    def notification_answer_day(self,company):
            return f'Компания: {company} стоит '
                
    def notification_answer_2day(self,company):
        return f'Компания: {company} стоит '
        
    def notification_answer_week(self,company):
        return f'Компания: {company} стоит '

    


