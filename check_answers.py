import config_clone
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
        if text == config_clone.PRIMARYKEYBOARD[0]:
            objMarkup = Keyboards.CostomizeKeyboard()
            return objMarkup.generate_theory_markup(), 'Выбор темы'

        if text == config_clone.PRIMARYKEYBOARD[1]:
            objMarkup = Keyboards.CostomizeKeyboard()
            return objMarkup.generate_quote_markup(), 'Выбор валюты'

        if text == config_clone.PRIMARYKEYBOARD[2]:
            if self.existence_of_polling == 1:
                return None, 'Вы уже выбрали показ уведомлений'
            else:
                objMarkup = Keyboards.CostomizeKeyboard()
                return objMarkup.generate_notification_markup(), 'Выбор периода уведомлений' 

    #@classmethod
    def check_theory_answer(self,text):
        if text == config_clone.THEORYKEYBOARD[0]:
            return 'Здесь будет информация про инвестирование'
        
        if text == config_clone.THEORYKEYBOARD[1]:
            return 'Здесь будет информация про трейдинг'

    #@classmethod
    def check_quote_answer(self,company):
        #if text == config_clone.QUOTEKEYBOARD[0]:
        return self.storage.get_companies_data(company)
        
        #if text == config_clone.QUOTEKEYBOARD[1]:
            #return 'Здесь будет выводиться значение в рублях'

    #@classmethod
    def check_notification_answer(self,company):
        if text == config_clone.NOTIFICATIONKEYBOARD[0]:
            time.sleep(10)
            name_of_company = 'Sber'
            value_of_company = '130'
            return f'Компания: {name_of_company} стоит {value_of_company}'
                
        if text == config_clone.NOTIFICATIONKEYBOARD[1]:
            time.sleep(15)
            name_of_company = 'Sber'
            value_of_company = '150'
            return f'Компания: {name_of_company} стоит {value_of_company}'
        
        if text == config_clone.NOTIFICATIONKEYBOARD[2]:
            name_of_company = 'Sber'
            value_of_company = '160'
            return f'Компания: {name_of_company} стоит {value_of_company}'

    


