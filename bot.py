import time
import telebot
from telebot import types
import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
import config
from db_query import notification_list as ntflst
from db_query import state
from db_query import companies as cmp
from db_query import notification_state as ntf
import answer
import keyboards
from parse import stock_price_plot
from message_answers import read_messages

# объявление объекта бота
bot = telebot.TeleBot(config.token_test)

def send_notification(user_chat_id: int):
    """Аргументы: чат id пользователя
        Цель: Отправляет уведомление всех 
        компаний, добавленных в список.
    """
    companies = ntflst.get_notification_companies(user_chat_id)
    for company in companies:
        bot.send_message(user_chat_id,
            text=answer.quote_answer_currency(company[0]))

class Notification():
    """Класс для настройки уведомлений"""
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        # Объявление параметров отправки уведомлений
        jobstores = {'default': SQLAlchemyJobStore(
            url=f'sqlite:///{config.notification_db_path}')}
        executors = {
            'default': {'type': 'threadpool', 'max_workers': 20},
            'processpool': ProcessPoolExecutor(max_workers=20)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 20
        }
        # Применение настроек параметров отправки уведомлений
        self.scheduler.configure(jobstores=jobstores,
                                 executors=executors,
                                 job_defaults=job_defaults)

    def run_notification(self):
        """Функция отправки уведомления"""
        self.scheduler.start()
        try:
            # This is here to simulate application activity (which keeps the
            # main thread alive).
            while True:
                time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            print('exeption')
            # Not strictly necessary if daemonic mode is enabled but should be
            # done if possible
            self.scheduler.shutdown()

    def add_notification_day(self, user_chat_id: int, user_time: str):
        """
        Аргументы: чат id пользователя, время уведомления
        Цель: добавляет уведомление раз в день для
        пользователя.
        """
        self.scheduler.add_job(
            send_notification, 'interval',
            days=1, start_date=user_time,
            id=str(user_chat_id), jitter=40,
            args=[user_chat_id,])

    def add_notification_2days(self, user_chat_id: int, user_time: str):
        """
        Аргументы: чат id пользователя, время уведомления
        Цель: добавляет уведомление раз в 2 дня для
            пользователя.
        """
        self.scheduler.add_job(send_notification,
            'interval', days=2, start_date=user_time,
            id=str(user_chat_id), jitter=40,
            args=[user_chat_id,])

    def add_notification_week(self, user_chat_id: int, user_time: str):
        """
        Аргументы: чат id пользователя, время уведомления
        Цель: добавляет уведомление раз в неделю для
        пользователя.
        """
        self.scheduler.add_job(
            send_notification, 'interval', weeks=1,
            start_date=user_time, id=str(user_chat_id),
            jitter=40, args=[user_chat_id,])

    def delete_notification(self, user_chat_id: int):
        """
        Аргументы: чат id пользователя
        Цель: уведомление для пользователя
        """
        self.scheduler.remove_job(str(user_chat_id))

# объявление объекта уведомлений
notification = Notification()

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    """
    Принимает: Запрос от сервера при вводе @IMStockBot
    Цель: Показывать подсказки компаний из БД
    """
    # Смещение указателя при прокрутки
    offset = int(query.offset) if query.offset else 0
    # Компании из БД
    companies = cmp.get_companies_list(query.query, offset)
    m_next_offset = str(offset + 5) if len(companies) == 5 else None
    results_array = []
    try:
        for index, company in enumerate(companies):
            try:
                results_array.append(types.InlineQueryResultArticle(id=str(index),
                                           title=company[0],
                                           description= f"{company[1]} {company[2]}",
                                           input_message_content=types.InputTextMessageContent(
                                           message_text=company[0])))                                
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
    # Показ списка компаний в Inline режиме
    bot.answer_inline_query(query.id,results_array,
                            next_offset=m_next_offset if m_next_offset else "")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Принимает: Нажатие на команду /start
    Цель: Приветствие пользователя и показ функций бота
    """
    if not message.from_user.first_name and not message.from_user.last_name:
        bot.send_message(message.chat.id, text = f'''Добро пожаловать.''')
    elif not message.from_user.first_name and message.from_user.last_name: 
        bot.send_message(message.chat.id, text = f'''Добро пожаловать {message.from_user.last_name}.''')
    elif message.from_user.first_name and not message.from_user.last_name: 
        bot.send_message(message.chat.id, text = f'''Добро пожаловать {message.from_user.first_name}.''')
    else:
        bot.send_message(message.chat.id, text = f'''Добро пожаловать {message.from_user.first_name} \
                                                {message.from_user.last_name}.''')
    bot.send_message(message.chat.id, text=read_messages.get_message("start.txt"), parse_mode='HTML')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    """
    Принимает: Нажатие на команду /help.
    Цель: Отображение помощи для пользователя.
    """
    bot.send_message(message.chat.id, text=read_messages.get_message("help.txt"), parse_mode='html')
    from keyboards import keyboard_help
    bot.send_message(message.chat.id, text='Выберите команду',
                    reply_markup=keyboard_help.get_keyboard())


@bot.message_handler(commands=['set'])
def start_handler(message):
    """
    Принимает: Нажатие на команду /set.
    Цель: Отображение клавиатуры выбора функций. Фиксация состояния.
    """
    from keyboards.set import keyboard_primary
    bot.send_message(message.chat.id, text="Выберите опцию",
                    reply_markup=keyboard_primary.get_keyboard())
    # Фиксация состояния: Начальное
    state.set_state(message.chat.id, config.States.S_PRIMARY.value)
    bot.delete_message(message.chat.id, message.id)

@bot.message_handler(commands=['settings'])
def send_welcome(message):
    """
    Принимает: Нажатие на команду /settings.
    Цель: Отображение клавиатуры изменения настроек. Фиксация состояния.
    """
    bot.send_message(message.chat.id, 'Что ж, давайте поменяем настройки')
    from keyboards.settings import keyboard_settings
    bot.send_message(message.chat.id, text="Выберите настройку",
                    reply_markup=keyboards.settings.keyboard_settings.get_keyboard())
    # Фиксация состояния: Настройки
    state.set_state(message.chat.id, config.States.S_SETTINGS.value)
    bot.delete_message(message.chat.id, message.id)

# I уровень дерева
@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id)
                                                == config.States.S_PRIMARY.value)
def callback_primary(call):
    """
    Принимает: callback от кнопки клавиатуры первоначального состояния
    Цель: Обработка callback. Фиксация состояния. Вывод нужной клавиатуры.
    """
    if call.data == "Теория":
        from keyboards.set.theory import keyboard_theory
        bot.send_message(call.message.chat.id, text="Выберите теорию",
                        reply_markup=keyboard_theory.get_keyboard())
        # Фиксация состояния: Выбор теории
        state.set_state(call.message.chat.id, config.States.S_THEORY.value)
    if call.data == "Котировка":
        from keyboards.set.quote import keyboard_quote
        bot.send_message(call.message.chat.id, text = "Выберите валюту",
                        reply_markup=keyboard_quote.get_keyboard())
        # Фиксация состояния: Выбор котировки
        state.set_state(call.message.chat.id, config.States.S_QUOTE.value)
    if call.data == "Уведомление":
        notification_state = ntf.get_notification_state(call.message.chat.id)
        # Обработка существования уведомления
        if notification_state == 1:
            bot.send_message(call.message.chat.id,
                            text = f"У вас уже выбрано уведомление на \
                            {ntf.get_notification_time(call.message.chat.id)} \
                            раз в день (часовой пояс UTC+0).")
        elif notification_state == 2:
            bot.send_message(call.message.chat.id,
                            text=f"У вас уже выбрано уведомление на \
                            {ntf.get_notification_time(call.message.chat.id)} \
                            раз в 2 дня (часовой пояс UTC+0).")
        elif notification_state == 3:
            bot.send_message(call.message.chat.id,
                            text=f"У вас уже выбрано уведомление на \
                            {ntf.get_notification_time(call.message.chat.id)} \
                            раз в неделю (часовой пояс UTC+0).")  
        else:
            from keyboards.set.notification import keyboard_notification
            bot.send_message(call.message.chat.id, text="Выберите периодичность",
            reply_markup = keyboard_notification.get_keyboard())
            # Фиксация состояния: Установка уведомлений
            state.set_state(call.message.chat.id, config.States.S_NOTIFICATION.value)
    if call.data == "График":
        from keyboards.set.graph import keyboard_graph
        bot.send_message(call.message.chat.id, text="Выберите периодичность",
                        reply_markup=keyboard_graph.get_keyboard())
        # Фиксация состояния: Выбор графика
        state.set_state(call.message.chat.id, config.States.S_GRAPH.value)
    bot.delete_message(call.message.chat.id, call.message.id)

# II уровень дерева
@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id)
                                                ==config.States.S_THEORY.value)
def callback_theory(call):
    """
    Принимает: callback от кнопки клавиатуры выбора теории
    Цель: Обработка callback. Фиксация состояния. Вывод нужной теории.
    """
    if call.data == "Инвестирование":
        bot.send_message(call.message.chat.id, text=answer.theory_answer_investment())
        # Фиксация состояния: Теория по инвестированию
        state.set_state(call.message.chat.id, config.States.S_INVESTMENT.value)
    if call.data == "Трейдинг":
        bot.send_message(call.message.chat.id, text=answer.theory_answer_trading())
        # Фиксация состояния: Теория по трейдингу
        state.set_state(call.message.chat.id, config.States.S_TRADING.value)
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id)
                                                ==config.States.S_QUOTE.value)
def callback_quote(call):
    """
    Принимает: callback от кнопки клавиатуры выбора котировки
    Цель: Обработка callback. Фиксация состояния. Вывод нужной котировки.
    """
    if call.data == "Рубль":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_company.txt"))
        # Фиксация состояния: Получение котировки в рублях
        state.set_state(call.message.chat.id, config.States.S_RUBLE.value)
    if call.data == "Валюта":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_company.txt"))
        # Фиксация состояния: Получение котировки в исходной валюте
        state.set_state(call.message.chat.id, config.States.S_CURRENCY.value)
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id)
                                                == config.States.S_NOTIFICATION.value)
def callback_notification(call):
    """
    Принимает: callback от кнопки клавиатуры выбора уведомления
    Цель: Обработка callback. Фиксация состояния. Вывод выбора времени.
    """
    if call.data == "День":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_time.txt"), parse_mode='HTML')
        # Фиксация состояния раз в день
        state.set_state(call.message.chat.id, config.States.S_TIME_DAY.value)
    if call.data == "2Дня":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_time.txt"), parse_mode='HTML')
        # Фиксация состояния раз в два дня
        state.set_state(call.message.chat.id, config.States.S_TIME_2DAYS.value)
    if call.data == "Неделя":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_time.txt"), parse_mode='HTML')
        # Фиксация состояния раз в месяц
        state.set_state(call.message.chat.id, config.States.S_TIME_WEEK.value)
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id)
                                                == config.States.S_GRAPH.value)
def callback_graph(call):
    """
    Принимает: callback от кнопки клавиатуры выбора графика
    Цель: Обработка callback. Фиксация состояния. Вывод выбора компаний.
    """
    if call.data == "ГНеделя":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_company.txt"))
        # Фиксация состояния: График за неделю
        state.set_state(call.message.chat.id, config.States.S_GWEEK.value)
    if call.data == "ГМесяц":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_company.txt"))
        # Фиксация состояния: График за месяц
        state.set_state(call.message.chat.id, config.States.S_GMONTH.value)
    if call.data == "ГГод":
        bot.send_message(call.message.chat.id,
                        text=read_messages.get_message("choose_company.txt"))
        # Фиксация состояния: График за год
        state.set_state(call.message.chat.id, config.States.S_GYEAR.value)
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id)
                                                == config.States.S_SETTINGS.value)
def callback_settings(call):
    """
    Принимает: callback от кнопки клавиатуры выбора настроек
    Цель: Обработка callback. Фиксация состояния. Вывод нужной клавиатуры.
    """
    if call.data == "НКомпании":
        notification_list = ntflst.get_notification_list(call.message.chat.id)
        if notification_list:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id,
                            text="Выбранный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(call.message.chat.id, text=notification_list)
            from keyboards.settings.change_companies import keyboard_change_companies
            bot.send_message(call.message.chat.id, text="Выберите тип изменения",
                        reply_markup=keyboard_change_companies.get_keyboard())
            # Фиксация состояния: Изменения компаний 
            state.set_state(call.message.chat.id, config.States.S_CHANGE_COMPANIES.value)
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id,
            text=read_messages.get_message("add_companies.txt"), parse_mode='html')
            # Фиксация состояния: Добавления компаний 
            state.set_state(call.message.chat.id, config.States.S_ADD_COMPANIES.value)
    if call.data == "НУведомления":
        if not ntf.get_notification_state(call.message.chat.id):
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(call.message.chat.id,
            text="У вас нет выбранных уведомлений:(\
                Можете настроить их используя <b>/set</b>", parse_mode='html')
            # Фиксация состояния: Начало
            state.set_state(call.message.chat.id, config.States.S_START.value)
        else:
            bot.delete_message(call.message.chat.id, call.message.id)
            notification.delete_notification(call.message.chat.id)
            # Фиксация отсутствия уведомлений в БД
            ntf.set_notification_state(call.message.chat.id, config.NotificationStates.NS_NONE.value)
            bot.send_message(call.message.chat.id, text="Уведомление было успешно удалено:)")
            # Фиксация состояния: Начало
            state.set_state(call.message.chat.id, config.States.S_START.value)

@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id) 
                                                == config.States.S_CHANGE_COMPANIES.value)
def callback_changing(call):
    """
    Принимает: callback от кнопки клавиатуры выбора изменения компаний
    Цель: Обработка callback. Фиксация состояния. Вывод нужной клавиатуры.
    """
    if call.data == "ДобавитьКомпании":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 
                        text = read_messages.get_message("choose_company.txt"), parse_mode='html')
        # Фиксация состояния добвления
        state.set_state(call.message.chat.id, config.States.S_ADD_COMPANIES.value)
    if call.data == "УдалитьКомпании":
        from keyboards.settings.delete_companies import keyboard_delete_companies
        bot.send_message(call.message.chat.id, text = "Выберите опцию удаления",
            reply_markup=keyboard_delete_companies.get_keyboard())
        # Фиксация состояния удаления
        state.set_state(call.message.chat.id, config.States.S_DELETE_COMPANIES.value)
        bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func = lambda call: state.get_current_state(call.message.chat.id) 
                                                == config.States.S_DELETE_COMPANIES.value)
def callback_deletion(call):
    """
    Принимает: callback от кнопки клавиатуры выбора удаления компаний
    Цель: Обработка callback. Фиксация состояния. 
    """
    if call.data == "УдалитьВсе":
        bot.delete_message(call.message.chat.id, call.message.id)
        # Удаление компаний у пользователя
        ntflst.delete_all_members(call.message.chat.id)
        bot.send_message(call.message.chat.id,text = "Список компаний для уведомлений успешно удалён")
        # Фиксация состояния: Начало
        state.set_state(call.message.chat.id, config.States.S_START.value)
    if call.data == "УдалитьВыборочно":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id,
        text=read_messages.get_message("delete_companies.txt"), parse_mode='HTML')
        # Фиксация состояния удаления выборочно
        state.set_state(call.message.chat.id, config.States.S_DELETE_SELECTIVELY.value)


@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id)
                                        == config.States.S_RUBLE.value)
def get_company_ruble(message):
    """
    Принимает: сообщение с названием компании
    Цель: Получение котировки в рублях и вывод в сообщении. 
    """
    try:
        # Вывод котировки в рублях
        bot.send_message(message.chat.id, text = answer.quote_answer_ruble(message.text))
        # Фиксация состояния: Начало
        state.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id,
        text='Упс, похоже вы ввели неправильное название компании. \
            Попробуйте ввести название компании еще раз:(')
    except AttributeError:
        bot.send_message(message.chat.id,
        text='Упс, что-то пошло не так. \
            Напишите об этом @mishlen25. \
            Произошло несоответствие базы данных компаний с существующими компаниями')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id)
                                        == config.States.S_CURRENCY.value)
def get_company_currency(message):
    """
    Принимает: сообщение с названием компании
    Цель: Получение котировки в исходной валюте и вывод в сообщении. 
    """
    try:
        bot.send_message(message.chat.id, text = answer.quote_answer_currency(message.text))
        # Фиксация состояния: Начало
        state.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id,
        text='Упс, похоже вы ввели неправильное название компании. \
            Попробуйте ввести компании еще раз:(')
    except AttributeError:
        bot.send_message(message.chat.id,
        text='Упс, что-то пошло не так. Напишите об этом @mishlen25. \
        Произошло несоответствие базы данных компаний с существующими компаниями в yahoo.finance')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id)
                                        == config.States.S_TIME_DAY.value)
def time_notification_day(message):
    """
    Принимает: Cообщение со временем получения котировки в формате:
    %H:%M
    Цель: Обработка сообщения, установка уведомления раз в день и выбор списка компаний. 
    """
    try:
        # Парсинг времени
        user_time = datetime.strptime(message.text, "%H:%M")
        user_time = datetime.today().replace(hour = user_time.hour, minute=user_time.minute, second=0)
        # Фиксация времени
        ntf.set_notification_time(message.chat.id, user_time)
    except ValueError:
        bot.send_message(message.chat.id,
                text = "Ой, кажется вы ввели неправильное время. \
                    Введите удобное для вас время еще раз:(")
        return
    # Установка уведомления раз в день
    notification.add_notification_day(message.chat.id, user_time)
    # Фиксация времени в БД
    ntf.set_notification_state(message.chat.id, config.NotificationStates.NS_DAY.value)
    ntf.set_notification_time(message.chat.id, message.text)
    bot.send_message(message.chat.id,
                    text="Выбор времени произошел удачно. \
                    Выберите список компаний, которые хотите добавить в уведомление.")
    # Получения списка выбранных ранее компаний
    notification_list = ntflst.get_notification_list(message.chat.id)
    if notification_list:
        bot.send_message(message.chat.id,
                        text="Выбранный вами ранее список компаний (Название - Тикер - Биржа)")
        bot.send_message(message.chat.id, text=notification_list)
        bot.send_message(message.chat.id, text=read_messages.get_message('choose_companies.txt'),
                                        parse_mode='html')
    else: 
        bot.send_message(message.chat.id, text='''У вас нет выбранных ранее компаний.
                                                Давайте добавим несколько:)\n
                                                Введите список компаний, которые хотите добавить.
                                                Чтобы получить подсказку напишите: @IMStockBot,
                                                затем пробел и затем начните вводить название.
                                                Список существующих компаний будет предложен выше:) 
                                                Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')
    # Фиксация состояния выбора компаний
    state.set_state(message.chat.id, config.States.S_COMPANIES.value)

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id)
                                        == config.States.S_TIME_2DAYS.value)
def time_notification_2days(message):
    """
    Принимает: Cообщение со временем получения котировки в формате:
    %H:%M
    Цель: Обработка сообщения, установка уведомления раз в 2 дня и выбор списка компаний. 
    """
    try:
        # Парсинг времени
        user_time = datetime.strptime(message.text, "%H:%M")
        user_time = datetime.today().replace(hour = user_time.hour, minute=user_time.minute, second=0)
        # Фиксация времени
        ntf.set_notification_time(message.chat.id, user_time)
    except ValueError:
        bot.send_message(message.chat.id, text = "Ой, кажется вы ввели неправильное время. \
                                                Введите удобное для вас время еще раз:(")
        return
    # Установка уведомления раз в 2 дня
    notification.add_notification_2days(message.chat.id, user_time)
    # Фиксация времени в БД
    ntf.set_notification_state(message.chat.id, config.NotificationStates.NS_2DAYS.value)
    ntf.set_notification_time(message.chat.id, message.text)
    bot.send_message(message.chat.id,
                    text="Выбор времени произошел удачно. \
                        Выберите список компаний, которые хотите добавить в уведомление.")
    # Получение списка выбранных ранее компаний
    notification_list = ntflst.get_notification_list(message.chat.id)
    if notification_list:
        bot.send_message(message.chat.id, text="Выбранный вами ранее список компаний (Название - Тикер - Биржа)")
        bot.send_message(message.chat.id, text=notification_list)
        bot.send_message(message.chat.id,
                        text=read_messages.get_message('choose_companies.txt'), parse_mode='html')
    else: 
        bot.send_message(message.chat.id,
                        text='''У вас нет выбранных ранее компаний. \
                            Давайте добавим несколько:)\n Введите список компаний,
                            которые хотите добавить. Чтобы получить подсказку напишите: @IMStockBot,
                            затем пробел и затем начните вводить название.
                            Список существующих компаний будет предложен выше:)
                            Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')
    # Фиксация состояния: Выбор компаний
    state.set_state(message.chat.id, config.States.S_COMPANIES.value)

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) 
                                        == config.States.S_TIME_WEEK.value)
def time_notification_week(message):
    """
    Принимает: Cообщение со временем получения котировки в формате:
    %H:%M
    Цель: Обработка сообщения, установка уведомления раз в 2 дня и выбор списка компаний. 
    """
    try:
        # Парсинг времени
        user_time = datetime.strptime(message.text, "%H:%M")
        # Фиксация времени в БД
        user_time = datetime.today().replace(hour = user_time.hour, minute=user_time.minute, second=0)
        # Получение списка выбранных ранее компаний
        ntf.set_notification_time(message.chat.id, user_time)
    except ValueError:
        bot.send_message(message.chat.id,
                        text="Ой, кажется вы ввели неправильное время. \
                            Введите удобное для вас время еще раз:(")
        return
    # Получение списка выбранных ранее компаний
    notification.add_notification_week(message.chat.id, user_time)
    # Фиксация времени в БД
    ntf.set_notification_state(message.chat.id, config.NotificationStates.NS_WEEK.value)
    ntf.set_notification_time(message.chat.id, message.text)
    bot.send_message(message.chat.id,
                    text="Выбор времени произошел удачно. \
                        Выберите список компаний, которые хотите добавить в уведомление.")
    # Получение списка выбранных ранее компаний
    notification_list = ntflst.get_notification_list(message.chat.id)
    if notification_list:
        bot.send_message(message.chat.id,
                        text="Выбранный вами ранее список компаний (Название - Тикер - Биржа)")
        bot.send_message(message.chat.id, text=notification_list)
        bot.send_message(message.chat.id, text=read_messages.get_message('choose_companies.txt'), parse_mode='html')
    else: 
        bot.send_message(message.chat.id,
                        text='''У вас нет выбранных ранее компаний. \
                                Давайте добавим несколько:)\n \
                                Введите список компаний, которые хотите добавить. \
                                Чтобы получить подсказку напишите: @IMStockBot, затем \
                                пробел и затем начните вводить название. \
                                Список существующих компаний будет предложен выше:) \
                                Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='html')
    #Фиксация состояния: Выбор компаний
    state.set_state(message.chat.id, config.States.S_COMPANIES.value)

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id)
                                    == config.States.S_COMPANIES.value)
def company_notification(message):
    """
    Принимает: Cообщение с названием компании
    Цель: Добавление компаниии в список уведомлений
    """
    if message.text!='Хватит':
        try:
            # Установление значения в БД
            ntflst.set_notification_member(message.chat.id, message.text)
            bot.send_message(message.chat.id,
                            text='Отлично. Я запомнил. \
                                    Может выберем что-то еще или напишите <b>Хватит</b>',
                            parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id,
                            text ='Упс, похоже вы ввели неправильное название компании.\
                            Попробуйте ввести название компании еще раз:(')
    else:
        # Список выбранных пользователем компаний
        notification_list = ntflst.get_notification_list(message.chat.id)
        if notification_list:
            bot.send_message(message.chat.id, text="Выбранный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(message.chat.id, text=notification_list)
            bot.send_message(message.chat.id, text="Ожидайте получения уведомлений:)")
            # Фиксация состояния: Начало
            state.set_state(message.chat.id, config.States.S_START.value)
        else: 
            bot.send_message(message.chat.id,
                            text='''Кажется вы ничего не выбрали.\n\
                                Введите список компаний, которые хотите добавить в уведомления.\n\
                                Чтобы прекратить ввод, напишите: <b>Хватит</b>''',
                            parse_mode='HTML')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) 
                                            == config.States.S_GWEEK.value)
def get_graph_week(message):
    """
    Принимает: Cообщение с названием компании
    Цель: Отображение графика за неделю для данной компании
    """
    try:
        # Сохранение графика в виде изображения
        stock_price_plot.get_week_plot(message.text,message.chat.id)
        with open(f"{config.image_path}/{message.chat.id}.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo)
        # Фиксация состояния
        state.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id,
                        text='Упс, похоже вы ввели неправильное название компании. \
                        Попробуйте ввести название компании еще раз:(')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id)
                                    == config.States.S_GMONTH.value)
def get_graph_month(message):
    """
    Принимает: Cообщение с названием компании
    Цель: Отображение графика за месяц для данной компании
    """
    try:
        # Сохранение графика в виде изображения
        stock_price_plot.get_month_plot(message.text,message.chat.id)
        with open(f"{config.image_path}/{message.chat.id}.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo)
        # Фиксация состояния
        state.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id,
                        text='Упс, похоже вы ввели неправильное название компании. \
                            Попробуйте ввести название компании еще раз:(')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) == config.States.S_GYEAR.value)
def get_graph_year(message):
    """
    Принимает: Cообщение с названием компании
    Цель: Отображение графика за год для данной компании
    """
    try:
        # Сохранение графика в виде изображения
        stock_price_plot.get_year_plot(message.text,message.chat.id)
        with open(f"{config.image_path}/{message.chat.id}.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo = photo)
        # Фиксация состояния
        state.set_state(message.chat.id, config.States.S_START.value)
    except TypeError:
        bot.send_message(message.chat.id,
                        text='Упс, похоже вы ввели неправильное название компании. \
                            Попробуйте ввести название компании еще раз:(')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) 
                                        == config.States.S_ADD_COMPANIES.value)
def company_add(message):
    """
    Принимает: Cообщение с названием компании
    Цель: Добавление компаниии в список уведомлений при его изменении
    """
    if message.text!='Хватит':
        try:
            ntflst.set_notification_member(message.chat.id, message.text)
            bot.send_message(message.chat.id,
                            text='Отлично. Я запомнил. \
                            Может выберем что-то еще или напишите <b>Хватит</b>', parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id, text = 'Упс, похоже вы ввели неправильное название компании. Попробуйте ввести название компании еще раз:(')
    else:
        notification_list = ntflst.get_notification_list(message.chat.id)
        if notification_list:
            bot.send_message(message.chat.id, text = "Выбранный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(message.chat.id, text = notification_list)
            state.set_state(message.chat.id, config.States.S_START.value)
        else: 
            bot.send_message(message.chat.id,
                            text='''Кажется вы ничего не выбрали.\n
                                Введите список компаний, которые хотите добавить в уведомления.\n
                            Чтобы прекратить ввод, напишите: <b>Хватит</b>''', parse_mode='HTML')

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) 
                                        == config.States.S_DELETE_SELECTIVELY.value)
def company_delete_selectively(message):
    """
    Принимает: Cообщение с названием компании
    Цель: Удаляет компаниии из списка уведомлений
    """
    if message.text!='Хватит':
        try:
            ntflst.delete_selectively_member(message.chat.id, message.text)
            bot.send_message(message.chat.id,
                            text='Отлично. Я удалил. Может удалим что-то еще или напишите <b>Хватит</b>',
                            parse_mode='HTML')
        except TypeError:
            bot.send_message(message.chat.id,
                            text='Упс, похоже вы ввели неправильное название компании. \
                                Попробуйте ввести название компании еще раз:(',
                            parse_mode='HTML')
        except AttributeError: 
            bot.send_message(message.chat.id,\
                            text='Упс, похоже такой компании у вас нет. \
                                Попробуйте ввести название компании еще раз или напишите <b>Хватит</b>',
                            parse_mode='HTML')
    else:
        #  Получения списка уведомлений
        notification_list = ntflst.get_notification_list(message.chat.id)
        if notification_list:
            bot.send_message(message.chat.id,
                            text="Измененный вами список компаний (Название - Тикер - Биржа)")
            bot.send_message(message.chat.id, text = notification_list)
        else: 
            bot.send_message(message.chat.id,
                            text='''Кажется вы удалили все компании в вашем списке:(
                                Вы знаете, где их настроить в случае чего:)''')
        state.set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: state.get_current_state(message.chat.id) 
                                            == config.States.S_START.value)
def handle_start_state(message):
    """Обработка начального положения"""
    bot.send_message(message.chat.id,
    text=read_messages.get_message("initial_position.txt"), parse_mode='HTML')

if __name__ == '__main__':
    """Запуск приложения"""
    try:
        # Паралеллизация потоков
        t1 = threading.Thread(target=notification.run_notification, args=[])
        # Запуск отслеживания уведомлений
        t1.start()
        # Запуск бота
        bot.infinity_polling()
    except:
        pass
