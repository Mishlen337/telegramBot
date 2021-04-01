import config
import telebot
from telebot import types
import answer
import time
import stock_price_plot
import dbworker
from datetime import datetime

import threading

from pytz import utc
import time
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

bot = telebot.TeleBot(config.token)

def send_notification(user_chat_id:int):
        companies = dbworker.get_notification_companies(user_chat_id)
        for company in companies:
            bot.send_message(user_chat_id, text = answer.quote_answer_currency(company[0]))


class Notification():
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs2.sqlite')
            }
        executors = {
                'default': {'type': 'threadpool', 'max_workers': 20},
                'processpool': ProcessPoolExecutor(max_workers=5)
            }
        job_defaults = {
                'coalesce': False,
                'max_instances': 3
            }

        self.scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    def run_notification(self):
        self.scheduler.start()
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            print('exeption')
                # Not strictly necessary if daemonic mode is enabled but should be done if possible
            self.scheduler.shutdown()
    
    def add_notification_day(self, user_chat_id:int, time:str):
        self.scheduler.add_job(send_notification, 'interval', minutes=1, id=str(user_chat_id), args = [user_chat_id,])

    def add_notification_2days(self, user_chat_id:int, time:str):
        self.scheduler.add_job(send_notification, 'interval', minutes=2, id=str(user_chat_id), args = [user_chat_id,])

    def add_notification_week(self, user_chat_id:int, time:str):
        self.scheduler.add_job(send_notification, 'interval', minutes=3, id=str(user_chat_id), args = [user_chat_id,])
    
    def delete_notification(self, user_chat_id:int):
        self.scheduler.remove_job(str(user_chat_id))

notification = Notification()   

keyboard_help = types.ReplyKeyboardMarkup(row_width=3)
button_set = types.KeyboardButton('/set')
button_settings = types.KeyboardButton('/settings')
button_help = types.KeyboardButton('/help')
keyboard_help.add(button_set,button_settings,button_help)




""" Инициализация начальной клавиатуры """
keyboard_primary = types.InlineKeyboardMarkup(row_width=1)
button_theory = types.InlineKeyboardButton(text = "Теория", callback_data = "Теория")
button_quote = types.InlineKeyboardButton(text = "Получение одной котировки", callback_data = "Котировка")
button_graph = types.InlineKeyboardButton(text = "Построение графика", callback_data = "График")
button_notification = types.InlineKeyboardButton(text = "Настройка уведомлений", callback_data = "Уведомление")
keyboard_primary.add(button_theory, button_quote, button_graph, button_notification)


""" Инициализация клавиатуры теории """ 
keyboard_theory = types.InlineKeyboardMarkup(row_width=1)
button_investment = types.InlineKeyboardButton(text = "Инвестирование", callback_data = "Инвестирование")
button_trading = types.InlineKeyboardButton(text = "Трейдинг", callback_data = "Трейдинг")
keyboard_theory.add(button_investment, button_trading)

""" Инициализация клавиатуры котировки """
keyboard_quote = types.InlineKeyboardMarkup(row_width=1)
button_ruble = types.InlineKeyboardButton(text = "В рублях", callback_data = "Рубль")
button_currency = types.InlineKeyboardButton(text = "В исходной валюте", callback_data = "Валюта")
keyboard_quote.add(button_ruble, button_currency)

""" Инициализация клавиатуры уведомлений """
keyboard_notification = types.InlineKeyboardMarkup(row_width=1)
button_day = types.InlineKeyboardButton(text = "Раз в день", callback_data = "День")
button_2days = types.InlineKeyboardButton(text = "Раз в два дня", callback_data = "2Дня")
button_week = types.InlineKeyboardButton(text = "Раз в неделю", callback_data = "Неделя")
keyboard_notification.add(button_day, button_2days, button_week)

""" Инициализация клавиатуры графика """
keyboard_graph = types.InlineKeyboardMarkup(row_width=1)
button_gweek = types.InlineKeyboardButton(text = "За неделю", callback_data = "ГНеделя")
button_gmonth = types.InlineKeyboardButton(text = "За месяц", callback_data = "ГМесяц")
button_gyear = types.InlineKeyboardButton(text = "За год", callback_data = "ГГод")
keyboard_graph.add(button_gweek, button_gmonth, button_gyear)

""" Инициализация клавиатуры настроек """
keyboard_settings = types.InlineKeyboardMarkup(row_width=1)
button_companies = types.InlineKeyboardButton(text = "Изменить список компаний", callback_data = "НКомпании")
button_notification = types.InlineKeyboardButton(text = "Отменить посылку уведомлений", callback_data = "НУведомления")
keyboard_settings.add(button_companies, button_notification)

""" Инициализация клавиатуры изменения компаний """
keyboard_change_companies = types.InlineKeyboardMarkup(row_width=1)
button_add_companies = types.InlineKeyboardButton(text = "Добавить компании", callback_data = "ДобавитьКомпании")
button_delete_companies = types.InlineKeyboardButton(text = "Удалить компании", callback_data = "УдалитьКомпании")
keyboard_change_companies.add(button_add_companies, button_delete_companies)

""" Инициализация клавиатуры удаления компаний """
keyboard_delete_companies = types.InlineKeyboardMarkup(row_width=1)
button_all = types.InlineKeyboardButton(text = "Удалить все", callback_data = "УдалитьВсе")
button_selectively = types.InlineKeyboardButton(text = "Удалить выборочно", callback_data = "УдалитьВыборочно")
keyboard_delete_companies.add(button_all, button_selectively)

#Помощь при вводе компании
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    offset = int(query.offset) if query.offset else 0
    companies = dbworker.get_companies_list(query.query, offset)
    m_next_offset = str(offset + 5) if len(companies) == 5 else None
    results_array = []
    try:
        for index, company in enumerate(companies):
            try:
                
                results_array.append(types.InlineQueryResultArticle(id=str(index),
                                           title=company[0],
                                           description= f"{company[1]} {company[2]}",
                                           input_message_content=types.InputTextMessageContent(
                                           message_text=company[0]
                                           )
                                        )
                                    )                   
                                    
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    bot.answer_inline_query(query.id, results_array, next_offset=m_next_offset if m_next_offset else "")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, text = f'''Добро пожаловать {message.from_user.first_name} {message.from_user.last_name}.\n
<b>ОБЯЗАТЕЛЬНО прочтите это сообщение перед первым использованием</b>\n
Давайте я расскажу немного о себе.
Я умный помошник в сфере акций. Мой функционал заключается в следующем:\n
1. Прохождение теории по трейдингу и инвестированию\n
2. Получение котировки акции в разных валютах в реальном времени\n
3. Построение графика за различные промежутки времени\n
4. Настройка уведомлений с выбранном списком акций\n
Чтобы узнать как пользоваться вышеописанными фунциями, напишите <b>/help</b>''', parse_mode='HTML')
    bot.send_message(message.chat.id, text = 'Выберите опцию', reply_markup = keyboard_help)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text = '''Вы зашли в режим помощи.ляллял\n
1. Чтобы выбрать выбрать мой функционал напишите <b>/set</b>\n
2. Чтобы изменить список компаний, входящих в уведомления или отменить посылку уведомлений напишите <b>/settings</b>\n
В случае неиспровностей, вопросов и предложениий обращайтесь к Исакову Михаилу - @mishlen25''', parse_mode='html')


""" Отправка начальной клавиатуры """
@bot.message_handler(commands=['set'])
def start_handler(message):
    bot.send_message(message.chat.id, text = "Выберите опцию", reply_markup=keyboard_primary)
    dbworker.set_state(message.chat.id, config.States.S_PRIMARY.value)
    bot.delete_message(message.chat.id, message.id)

@bot.message_handler(commands=['settings'])
def send_welcome(message):
    bot.reply_to(message, 'Что ж, давайте поменяем настройки')
    bot.send_message(message.chat.id, text = "Выберите опцию", reply_markup=keyboard_settings)
    dbworker.set_state(message.chat.id, config.States.S_SETTINGS.value)
    bot.delete_message(message.chat.id, message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_PRIMARY.value)
def callback_primary(call):
    if call.data == "Теория": 
        bot.send_message(call.message.chat.id, text = "Выберите теорию", reply_markup = keyboard_theory)
        dbworker.set_state(call.message.chat.id, config.States.S_THEORY.value)
        
    if call.data == "Котировка":
        bot.send_message(call.message.chat.id, text = "Выберите валюту", reply_markup = keyboard_quote)
        dbworker.set_state(call.message.chat.id, config.States.S_QUOTE.value)

    if call.data == "Уведомление":
        if not dbworker.get_notification_state:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = '''Вы уже выбрали уведомление на время  раз {вствить периодичность}. Если хотите поменять настройки напишите <b>/settings</b>''', parse_mode = 'HTML')
            dbworker.set_state(call.message.chat.id, config.States.S_START.value)
            return
        bot.send_message(call.message.chat.id, text = "Выберите периодичность", reply_markup = keyboard_notification)
        dbworker.set_state(call.message.chat.id, config.States.S_NOTIFICATION.value)
        
    if call.data == "График":
        bot.send_message(call.message.chat.id, text = "Выберите периодичность", reply_markup = keyboard_graph)
        dbworker.set_state(call.message.chat.id, config.States.S_GRAPH.value)
    
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_THEORY.value)
def callback_theory(call):
    """ Отправка информации по теории """
    if call.data == "Инвестирование":
        bot.send_message(call.message.chat.id, text = answer.theory_answer_investment())
        dbworker.set_state(call.message.chat.id, config.States.S_INVESTMENT.value)

    if call.data == "Трейдинг":
        bot.send_message(call.message.chat.id, text = answer.theory_answer_trading())
        dbworker.set_state(call.message.chat.id, config.States.S_TRADING.value)

    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_QUOTE.value)
def callback_quote(call):
    """ Отправка информации по котеровки """
    if call.data == "Рубль":
        bot.send_message(call.message.chat.id, text = "Введите название компании. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:)")
        dbworker.set_state(call.message.chat.id, config.States.S_RUBLE.value)

    if call.data == "Валюта":
        bot.send_message(call.message.chat.id, text = "Введите название компании. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:)")
        dbworker.set_state(call.message.chat.id, config.States.S_CURRENCY.value)

    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_NOTIFICATION.value)
def callback_notification(call):
    """Отправка уведомлений котеровок"""
    if call.data == "День":
        notification_list = dbworker.get_notification_list(call.message.chat.id)
        if notification_list:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Выбранный вами ранее список компаний (Название - Тикер - Биржа)")
            bot.send_message(call.message.chat.id, text = notification_list)
            bot.send_message(call.message.chat.id, text = '''Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод или оставить текущий список компаний, напишите: <b>Хватит</b>''', parse_mode='html')
        else: 
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = '''У вас нет выбранных ранее компаний. Давайте добавим несколько:)\n
Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')
        dbworker.set_state(call.message.chat.id, config.States.S_COMPANIES.value)
        dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_DAY.value)

    if call.data == "2Дня":
        notification_list = dbworker.get_notification_list(call.message.chat.id)
        if notification_list:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Выбранный вами ранее список компаний (Название - Тикер - Биржа)")
            bot.send_message(call.message.chat.id, text = notification_list)
            bot.send_message(call.message.chat.id, text = '''Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод или оставить текущий список компаний, напишите: <b>Хватит</b>''', parse_mode='html')        
        else: 
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = '''У вас нет выбранных ранее компаний. Давайте добавим несколько:)\n
Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')        
        dbworker.set_state(call.message.chat.id, config.States.S_COMPANIES.value)
        dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_2DAYS.value)

    if call.data == "Неделя":
        notification_list = dbworker.get_notification_list(call.message.chat.id)
        if notification_list:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Выбранный вами ранее список компаний (Название - Тикер - Биржа)")
            bot.send_message(call.message.chat.id, text = notification_list)
            bot.send_message(call.message.chat.id, text = '''Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод или оставить текущий список компаний, напишите: <b>Хватит</b>''', parse_mode='html')        
        else: 
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = '''У вас нет выбранных ранее компаний. Давайте добавим несколько:)\n
Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')        
        dbworker.set_state(call.message.chat.id, config.States.S_COMPANIES.value)
        dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_WEEK.value)

    

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_GRAPH.value)
def callback_graph(call):
    """ Отправка графика функции """
    if call.data == "ГНеделя":
        bot.send_message(call.message.chat.id, text = "Введите название компании. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:)")
        dbworker.set_state(call.message.chat.id, config.States.S_GWEEK.value)
       
    if call.data == "ГМесяц":
        bot.send_message(call.message.chat.id, text = "Введи компанию. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:)")
        dbworker.set_state(call.message.chat.id, config.States.S_GMONTH.value)
       
    if call.data == "ГГод":
        bot.send_message(call.message.chat.id, text = "Введи компанию. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:)")
        dbworker.set_state(call.message.chat.id, config.States.S_GYEAR.value)
        
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_SETTINGS.value)
def callback_settings(call):
    if call.data == "НКомпании":
        notification_list = dbworker.get_notification_list(call.message.chat.id)
        if notification_list:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = "Выбранный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(call.message.chat.id, text = notification_list)
            bot.send_message(call.message.chat.id, text = "Выберите тип изменения", reply_markup = keyboard_change_companies)
            dbworker.set_state(call.message.chat.id, config.States.S_CHANGE_COMPANIES.value)
        else: 
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id, text = '''Кажется у вас нет выбранных компаний. Давайте добавим несколько:)\n
Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')
            dbworker.set_state(call.message.chat.id, config.States.S_ADD_COMPANIES.value)
    
    if call.data == "НУведомления":
        try:
            bot.delete_message(call.message.chat.id, call.message.id)
            notification.delete_notification(call.message.chat.id)
            bot.send_message(call.message.chat.id, text = "Уведомление было успешно удалено:)")
            dbworker.set_notification_state(call.message.chat.id, config.NotificationStates.NS_NONE.value)
            dbworker.set_state(call.message.chat.id, config.States.S_START.value)
        except apscheduler.jobstores.base.JobLookupError:
            bot.send_message(call.message.chat.id, text = "У вас нет выбранных уведомлений:( Можете настроить их используя <b>/set</b>", parse_mode='html')
            dbworker.set_state(call.message.chat.id, config.States.S_START.value)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_CHANGE_COMPANIES.value)
def callback_changing(call):
    if call.data == "ДобавитьКомпании":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id,  text = "Введите список компаний, которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод, напишите: <b>Хватит</b>", parse_mode='html')
        dbworker.set_state(call.message.chat.id, config.States.S_ADD_COMPANIES.value)
    if call.data == "УдалитьКомпании":
        bot.send_message(call.message.chat.id,  text = "Выберите опцию удаления. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:)", reply_markup = keyboard_delete_companies)
        dbworker.set_state(call.message.chat.id, config.States.S_DELETE_COMPANIES.value)
        bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: dbworker.get_current_state(call.message.chat.id) == config.States.S_DELETE_COMPANIES.value)
def callback_deletion(call):
    if call.data == "УдалитьВсе":
        bot.delete_message(call.message.chat.id, call.message.id)
        dbworker.delete_all_members(call.message.chat.id)
        bot.send_message(call.message.chat.id,  text = "Список компаний для уведомлений успешно удалён")
        dbworker.set_state(call.message.chat.id, config.States.S_START.value)
    if call.data == "УдалитьВыборочно":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id,  text = '''Введите список компаний, которые хотите удалить. Чтобы получить подсказку напишите: @IMStockBot, затем пробел и затем начните вводить название. Список существующих компаний будет предложен выше:) Чтобы прекратить ввод для удаления, напишите: <b>Хватит</b>''', parse_mode='HTML')
        dbworker.set_state(call.message.chat.id, config.States.S_DELETE_SELECTIVELY.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def handle_start_state(message):
    bot.send_message(message.chat.id, text = '''Вы находитесь в начальном состоянии, напишите команду, чтобы начать взаимодействовать со мной.\n
Чтобы узнать, что я умею, напишите команду <b>/start</b>\n
Чтобы узнать какие команды использовать напишите команду <b>/help</b>''', parse_mode='HTML')

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_RUBLE.value)
def get_company_ruble(message):
    try:
        bot.send_message(message.chat.id, text = answer.quote_answer_ruble(message.text))
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')
    except AttributeError:
        bot.send_message(message.chat.id, text = 'Упс, что-то пошло не так. Напишите об этом @mishlen25. Произошло несоответствие базы данных компаний с существующими компаниями')


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CURRENCY.value)
def get_company_currency(message):
    try:
        bot.send_message(message.chat.id, text = answer.quote_answer_currency(message.text))
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести компании еще раз:(')
    except AttributeError:
        bot.send_message(message.chat.id, text = 'Упс, что-то пошло не так. Напишите об этом @mishlen25. Произошло несоответствие базы данных компаний с существующими компаниями в yahoo.finance')


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_COMPANIES.value)
def company_notification(message):
    if message.text!='Хватит':
        try:
            dbworker.set_notification_member(message.chat.id, message.text)
            bot.send_message(message.chat.id, text = 'Отлично. Я запомнил. Может быверем что-то еще или напишите <b>Хватит</b>', parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')
    else:
        notification_list = dbworker.get_notification_list(message.chat.id)
        if notification_list:
            bot.send_message(message.chat.id, text = "Выбранный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(message.chat.id, text = notification_list)
            bot.send_message(message.chat.id, text = "Введите удобное для вас время получения котировок акций")
            dbworker.set_state(message.chat.id, config.States.S_TIME.value)
        else: 
            bot.send_message(message.chat.id, text = '''Кажется вы ничего не выбрали.\n
Введите список компаний, которые хотите добавить в уведомления.\n
Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='HTML')


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_TIME.value)
def time_notification(message):
    try: 
        dbworker.set_notification_time(message.chat.id, datetime.strptime(message.text, "%H:%M"))
    except ValueError:
        bot.send_message(message.chat.id, text = "Ой, кажется вы ввели неправильное время. Введите удобное для вас время еще раз:(")
        return
    try:
        notification_state = dbworker.get_notification_state(message.chat.id)
        if notification_state == 1:
            notification.add_notification_day(message.chat.id, message.text)
        if notification_state == 2:
            notification.add_notification_2days(message.chat.id, message.text)
        if notification_state == 3:
            notification.add_notification_week(message.chat.id, message.text)
        bot.send_message(message.chat.id, text = "Выбор времени произошел удачно. Ожидайте получения уведомления:)")
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except apscheduler.jobstores.base.ConflictingIdError:
        bot.send_message(message.chat.id, text = '''Упс, что-то пошло не так. Напишите об этом @mishlen25. Произошло несоответствие данных в базе данных уведомлений и базе данных пользователей''', parse_mode = 'HTML')
        dbworker.set_state(message.chat.id, config.States.S_START.value)
   

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GWEEK.value)
def get_graph_week(message):
    try:
        stock_price_plot.get_week_plot(message.text,message.chat.id)
        with open(f"{config.image_path}/{message.chat.id}.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo = photo)
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except KeyError:
        bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GMONTH.value)
def get_graph_month(message):
    try:
        stock_price_plot.get_month_plot(message.text,message.chat.id)
        with open(f"{config.image_path}/{message.chat.id}.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo = photo)   
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except KeyError:
        bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GYEAR.value)
def get_graph_year(message):
    try:
        stock_price_plot.get_year_plot(message.text,message.chat.id)
        with open(f"{config.image_path}/{message.chat.id}.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo = photo)   
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except KeyError:
        bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ADD_COMPANIES.value)
def company_add(message):
    if message.text!='Хватит':
        try:
            dbworker.set_notification_member(message.chat.id, message.text)
            bot.send_message(message.chat.id, text = 'Отлично. Я запомнил. Может быверем что-то еще или напишите <b>Хватит</b>', parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')
    else:
        notification_list = dbworker.get_notification_list(message.chat.id)
        if notification_list:
            bot.send_message(message.chat.id, text = "Выбранный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(message.chat.id, text = notification_list)
            dbworker.set_state(message.chat.id, config.States.S_START.value)
        else: 
            bot.send_message(message.chat.id, text = '''Кажется вы ничего не выбрали.\n
Введите список компаний, которые хотите добавить в уведомления.\n
Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='HTML')

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_DELETE_SELECTIVELY.value)
def company_delete_selectively(message):
    if message.text!='Хватит':
        try:
            dbworker.delete_selectively_member(message.chat.id, message.text)
            bot.send_message(message.chat.id, text = 'Отлично. Я удалил. Может удалим что-то еще или напишите <b>Хватит</b>', parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(', parse_mode='HTML')
        except AttributeError: 
            bot.send_message(message.chat.id, text = 'Упс, похоже такой компании у вас нет. Попробуйте ввести название компании еще раз или напишите <b>Хватит</b>', parse_mode='HTML')
    else:
        notification_list = dbworker.get_notification_list(message.chat.id)
        if notification_list:
            bot.send_message(message.chat.id, text = "Измененный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(message.chat.id, text = notification_list)
        else: 
            bot.send_message(message.chat.id, text = '''Кажется вы удалили все компании в вашем списке:( Вы знаете, где их настроить в случае чего:)''')
        dbworker.set_state(message.chat.id, config.States.S_START.value)


if __name__ == '__main__':
    t1 = threading.Thread(target=notification.run_notification, args=[])
    t1.start()
    bot.infinity_polling()