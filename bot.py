import config
import telebot
import check_answers
import time
import finance
from telebot import types
bot = telebot.TeleBot(config.token)
answer = check_answers.Answers()
company = ""

""" Инициализация начальной клавиатуры """
keyboard_primary = types.InlineKeyboardMarkup()
button_theory = types.InlineKeyboardButton(text = "Теория", callback_data = "Теория")
button_quote = types.InlineKeyboardButton(text = "Получение одной котировки", callback_data = "Котировка")
button_graph = types.InlineKeyboardButton(text = "Построение графика", callback_data = "График")
button_notification = types.InlineKeyboardButton(text = "Настройка уведомлений", callback_data = "Уведомление")
keyboard_primary.add(button_theory, button_quote, button_graph, button_notification)


""" Инициализация изменений """ 
keyboard_change = types.InlineKeyboardMarkup()
button_change_notification = types.InlineKeyboardButton(text = "Изменить уведомления", callback_data = "ИУведомление")

""" Инициализация клавиатуры теории """ 
keyboard_theory = types.InlineKeyboardMarkup()
button_investment = types.InlineKeyboardButton(text = "Инвестирование", callback_data = "Инвестирование")
button_trading = types.InlineKeyboardButton(text = "Трейдинг", callback_data = "Трейдинг")
keyboard_theory.add(button_investment, button_trading)

""" Инициализация клавиатуры котировки """
keyboard_quote = types.InlineKeyboardMarkup()
button_ruble = types.InlineKeyboardButton(text = "В рублях", callback_data = "Рубль")
button_currency = types.InlineKeyboardButton(text = "В исходной валюте", callback_data = "Валюта")
keyboard_quote.add(button_ruble, button_currency)

""" Инициализация клавиатуры уведомлений """
keyboard_notification = types.InlineKeyboardMarkup()
button_day = types.InlineKeyboardButton(text = "Раз в день", callback_data = "День")
button_2days = types.InlineKeyboardButton(text = "Раз в два дня", callback_data = "2Дня")
button_week = types.InlineKeyboardButton(text = "Раз в неделю", callback_data = "Неделя")
keyboard_notification.add(button_day, button_2days, button_week)

""" Инициализация клавиатуры графика """
keyboard_graph = types.InlineKeyboardMarkup()
button_week = types.InlineKeyboardButton(text = "За неделю", callback_data = "ГНеделя")
button_year = types.InlineKeyboardButton(text = "За год", callback_data = "ГГод")
button_all = types.InlineKeyboardButton(text = "За все время", callback_data = "ГВсе")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Подсоеденен пользователь, {message.from_user.first_name}')


@bot.message_handler(commands = ['reset'])
def resset_values(message):
    bot.send_message(message.chat.id, text = "Изменить уведомления", )
    answer.existence_of_polling = 0


""" Отправка начальной клавиатуры """
@bot.message_handler(commands=['start'])
def create_inline_keyboard(message):
    bot.send_message(message.chat.id, text = "Выберите опцию", reply_markup=keyboard_primary)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "Теория": 
        bot.send_message(call.message.chat.id, text = "Выберите теорию", reply_markup = keyboard_theory)
        bot.delete_message(call.message.chat.id, call.message.id)
    
    if call.data == "Котировка":
        bot.send_message(call.message.chat.id, text = "Выберите валюту", reply_markup = keyboard_quote)
        bot.delete_message(call.message.chat.id, call.message.id)

    if call.data == "Уведомление":
        bot.send_message(call.message.chat.id, text = "Выбирите периодичность", reply_markup = keyboard_notification)
        bot.delete_message(call.message.chat.id, call.message.id)

    """ Отправка информации по теории """

    if call.data == "Инвестирование":
        bot.send_message(call.message.chat.id, text = answer.theory_answer_investment())
        bot.delete_message(call.message.chat.id, call.message.id)

    if call.data == "Трединг":
        bot.send_message(call.message.chat.id, text = answer.theory_answer_trading())
        bot.delete_message(call.message.chat.id, call.message.id)

    """ Отправка информации по котеровки """

    if call.data == "Рубль":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        bot.delete_message(call.message.chat.id, call.message.id)
        get_company_ruble()   

    if call.data == "Валюта":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        bot.delete_message(call.message.chat.id, call.message.id)
        get_company_currency()
        
    """ Отправка уведомлений котеровок """

    if call.data == "День":
        if answer.existence_of_polling == 0:
            answer.existence_of_polling = 1
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Введи компанию")
            get_company_day()
        else: 
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Уведомление выбрано")


    if call.data == "2Дня":
        if answer.existence_of_polling == 0:
            answer.existence_of_polling = 1
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Введи компанию")
            get_company_2days()
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Уведомление выбрано")


    if call.data == "Неделя":
        if answer.existence_of_polling == 0:
            answer.existence_of_polling = 1
            bot.delete_message(call.message.chat.id, call.message.id)
            msg = bot.send_message(call.message.chat.id, text = "Введи компанию")
            get_company_week()
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Уведомление выбрано")
            
def get_company_day():
    @bot.message_handler(content_types=["text"])
    def company(message):
       while answer.existence_of_polling == 1:
            bot.send_message(message.chat.id, text = answer.notification_answer(message.text))
            time.sleep(10)

def get_company_2day():
    @bot.message_handler(content_types=["text"])
    def company(message):
       while answer.existence_of_polling == 1:
            bot.send_message(message.chat.id, text = answer.notification_answer(message.text))
            time.sleep(20)

def get_company_week():
    @bot.message_handler(content_types=["text"])
    def company(message):
       while answer.existence_of_polling == 1:
            bot.send_message(message.chat.id, text = answer.notification_answer(message.text))
            time.sleep(30)

def get_company_currency():
    @bot.message_handler(content_types=["text"])
    def company(message):
        bot.send_message(message.chat.id, text = answer.quote_answer_currency(message.text))

def get_company_ruble():
    @bot.message_handler(content_types=["text"])
    def company(message):
        bot.send_message(message.chat.id, text = answer.quote_answer_ruble(message.text))








if __name__ == '__main__':
    bot.infinity_polling()