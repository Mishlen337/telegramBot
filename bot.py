import config
import telebot
import answer
import time
import finance
from telebot import types
import stock_price_plot
import dbworker

bot = telebot.TeleBot(config.token)
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
button_gweek = types.InlineKeyboardButton(text = "За неделю", callback_data = "ГНеделя")
button_gmonth = types.InlineKeyboardButton(text = "За месяц", callback_data = "ГМесяц")
button_gyear = types.InlineKeyboardButton(text = "За год", callback_data = "ГГод")
keyboard_graph.add(button_gweek, button_gmonth, button_gyear)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    print(type(message.chat.id))
    bot.reply_to(message, f'Я бот. Подсоеденен пользователь, {message.from_user.first_name}')


""" Отправка начальной клавиатуры """
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, text = "Выберите опцию", reply_markup=keyboard_primary)
    dbworker.set_state(message.chat.id, config.States.S_PRIMARY.value)
    bot.delete_message(message.chat.id, message.id)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Что ж, начнём по-новой")
    bot.send_message(message.chat.id, text = "Выберите опцию", reply_markup=keyboard_primary)
    dbworker.set_state(message.chat.id, config.States.S_PRIMARY.value)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_PRIMARY.value)
def callback_primary(call):
    if call.data == "Теория": 
        bot.send_message(call.message.chat.id, text = "Выберите теорию", reply_markup = keyboard_theory)
        dbworker.set_state(call.message.chat.id, config.States.S_THEORY.value)
        
    if call.data == "Котировка":
        bot.send_message(call.message.chat.id, text = "Выберите валюту", reply_markup = keyboard_quote)
        dbworker.set_state(call.message.chat.id, config.States.S_QUOTE.value)

    if call.data == "Уведомление":
        bot.send_message(call.message.chat.id, text = "Выбирите периодичность", reply_markup = keyboard_notification)
        dbworker.set_state(call.message.chat.id, config.States.S_NOTIFICATION.value)
        
    if call.data == "График":
        bot.send_message(call.message.chat.id, text = "Выбирите периодичность", reply_markup = keyboard_graph)
        dbworker.set_state(call.message.chat.id, config.States.S_GRAPH.value)
    
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_THEORY.value)
def callback_theory(call):
    """ Отправка информации по теории """
    if call.data == "Инвестирование":
        bot.send_message(call.message.chat.id, text = answer.theory_answer_investment())
        dbworker.set_state(call.message.chat.id, config.States.S_INVESTMENT.value)

    if call.data == "Трединг":
        bot.send_message(call.message.chat.id, text = answer.theory_answer_trading())
        dbworker.set_state(call.message.chat.id, config.States.S_TRADING.value)

    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_QUOTE.value)
def callback_quote(call):
    """ Отправка информации по котеровки """
    if call.data == "Рубль":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_state(call.message.chat.id, config.States.S_RUBLE.value)

    if call.data == "Валюта":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_state(call.message.chat.id, config.States.S_CURRENCY.value)

    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_NOTIFICATION.value)
def callback_notification(call):
    """Отправка уведомлений котеровок"""
    if call.data == "День":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_DAY.value)
        dbworker.set_state(call.message.chat.id, config.States.S_COMPANIES.value)


    if call.data == "2Дня":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_2DAYS.value)
        dbworker.set_state(call.message.chat.id, config.States.S_COMPANIES.value)
        

    if call.data == "Неделя":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_WEEK.value)
        dbworker.set_state(call.message.chat.id, config.States.S_COMPANIES.value)
        
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_GRAPH.value)
def callback_graph(call):
    """ Отправка графика функции """
    if call.data == "ГНеделя":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_state(call.message.chat.id, config.States.S_GWEEK.value)
       
    if call.data == "ГМесяц":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_state(call.message.chat.id, config.States.S_GMONTH.value)
       
    if call.data == "ГГод":
        bot.send_message(call.message.chat.id, text = "Введи компанию")
        dbworker.set_state(call.message.chat.id, config.States.S_GYEAR.value)
        
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_RUBLE.value)
def get_company_ruble(message):
    bot.send_message(message.chat.id, text = answer.quote_answer_ruble(message.text))
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CURRENCY.value)
def get_company_currency(message):
    bot.send_message(message.chat.id, text = answer.quote_answer_currency(message.text))
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_COMPANIES.value)
def company_notification(message):
    dbworker.set_notification_member(message.chat.id, message.text)
    bot.send_message(message.chat.id, text = "Введите удобное вам время получения котировок")
    dbworker.set_state(message.chat.id, config.States.S_TIME.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TIME.value)
def time_notification(message):
    dbworker.set_notification_time(message.chat.id, message.text)
    bot.send_message(message.chat.id, text = "Выбор времени произошел удачно. Ожидайте получения уведомления:)")
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GWEEK.value)
def get_graph_week(message):
    stock_price_plot.get_week_plot(message.text)
    with open('plot.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo = photo)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GMONTH.value)
def get_graph_month(message):
    stock_price_plot.get_month_plot(message.text)
    with open('plot.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo = photo)   
    dbworker.set_state(message.chat.id, config.States.S_START.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GYEAR.value)
def get_graph_year(message):
    stock_price_plot.get_year_plot(message.text)
    with open('plot.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo = photo)   
    dbworker.set_state(message.chat.id, config.States.S_START.value)

if __name__ == '__main__':
    bot.infinity_polling()