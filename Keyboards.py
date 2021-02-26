import telebot
class CostomizeKeyboard:
    def __init__(self,current_state = None):
        print('Клавиатура проиницилизирована')
        self.current_state = current_state

    def generate_primary_markup(self):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('Теория','Получение одной котировки','Настройка уведомлений')
        return markup

    def generate_theory_markup(self):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('Инвестирование','Трейдинг')
        return markup

    def generate_quote_markup(self):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('В исходной валюте', 'В рублях')
        return markup

    def generate_notification_markup(self):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('Раз в день', 'Раз в два дня','Раз в неделю')
        return markup
       

