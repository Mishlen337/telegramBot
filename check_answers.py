import config
import time
import telebot
import Keyboards
import finance

class Answers:
    def __init__(self):
        self.list_of_notifications = [0,0,0]
        self.existence_of_polling = 0
        self.storage = finance.Storage()
        self.storage.upload_storage()
    #@classmethod    
    def check_primary_answer(self,text):
        print('Производится проверка первоначальных настроек')
        if text == config.PRIMARYKEYBOARD[0]:
            objMarkup = Keyboards.CostomizeKeyboard()
            return objMarkup.generate_theory_markup(), 'Выбор темы'

        if text == config.PRIMARYKEYBOARD[1]:
            objMarkup = Keyboards.CostomizeKeyboard()
            return objMarkup.generate_quote_markup(), 'Выбор валюты'

        if text == config.PRIMARYKEYBOARD[2]:
            if self.existence_of_polling == 1:
                return None, 'Вы уже выбрали показ уведомлений'
            else:
                objMarkup = Keyboards.CostomizeKeyboard()
                return objMarkup.generate_notification_markup(), 'Выбор периода уведомлений' 

    #@classmethod
    def check_theory_answer(self,text):
        if text == config.THEORYKEYBOARD[0]:
            return 'Здесь будет информация про инвестирование'
        
        if text == config.THEORYKEYBOARD[1]:
            return 'Здесь будет информация про трейдинг'

    #@classmethod
    def check_quote_answer(self,company):
        #if text == config_clone.QUOTEKEYBOARD[0]:
        return self.storage.get_companies_data(company)
        
        #if text == config_clone.QUOTEKEYBOARD[1]:
            #return 'Здесь будет выводиться значение в рублях'

    #@classmethod
    def check_notification_answer(self,text,company):
        if text == config.NOTIFICATIONKEYBOARD[0]:
            time.sleep(10)
            return f'Компания: {company} стоит {self.storage.get_companies_data(company)}'
                
        if text == config.NOTIFICATIONKEYBOARD[1]:
            time.sleep(20)
            return f'Компания: {company} стоит {self.storage.get_companies_data(company)}'
        
        if text == config.NOTIFICATIONKEYBOARD[2]:
            time.sleep(30)
            return f'Компания: {company} стоит {self.storage.get_companies_data(company)}'

    


