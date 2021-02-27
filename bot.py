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
button_notification = types.InlineKeyboardButton(text = "Настройка уведомлений", callback_data = "Уведомление")
keyboard_primary.add(button_theory, button_quote, button_notification)
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
""" Инициализация клавиатуры уведомлени """
keyboard_notification = types.InlineKeyboardMarkup()
button_day = types.InlineKeyboardButton(text = "Раз в день", callback_data = "День")
button_2days = types.InlineKeyboardButton(text = "Раз в два дня", callback_data = "2Дня")
button_week = types.InlineKeyboardButton(text = "Раз в неделю", callback_data = "Неделя")
keyboard_notification.add(button_day, button_2days, button_week)

""" Отправка начальной клавиатуры """
@bot.message_handler(commands=['start'])
def create_inline_keyboard(message):
    bot.send_message(message.chat.id, text = "Выберите опцию", reply_markup=keyboard_primary)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    hendler_messages(call.message, call.data)

@bot.message_handler(content_types = ['text'])
def hendler_messages(message, reply = None):
    if reply == "Теория": 
        bot.send_message(message.chat.id, text = "Выберите теорию", reply_markup = keyboard_theory)
        bot.delete_message(message.chat.id, message.id)

    if reply == "Котировка":
        bot.send_message(message.chat.id, text = "Выберите валюту", reply_markup = keyboard_quote)
        bot.delete_message(message.chat.id, message.id)

    if reply == "Уведомление":
        bot.send_message(message.chat.id, text = "Выбирите периодичность", reply_markup = keyboard_notification)
        bot.delete_message(message.chat.id, message.id)

    """ Отправка информации по теории """

    if reply == "Инвестирование":
        bot.send_message(message.chat.id, text = answer.theory_answer_investment())
        bot.delete_message(message.chat.id, message.id)

    if reply == "Трединг":
        bot.send_message(message.chat.id, text = answer.theory_answer_trading())
        bot.delete_message(message.chat.id, message.id)

    """ Отправка информации по котеровки """

    if reply == "Рубль":
        bot.send_message(message.chat.id, text = answer.quote_answer_ruble(company))
        bot.delete_message(message.chat.id, message.id)

    if reply == "Валюта":
        bot.send_message(message.chat.id, text = answer.quote_answer_currency(company))
        bot.delete_message(message.chat.id, message.id)

    """ Отправка уведомлений котеровок """

    if reply == "День":
        if answer.existence_of_polling == 0:
            answer.existence_of_polling = 1
            bot.delete_message(message.chat.id, message.id)
            while answer.existence_of_polling == 1:
                bot.send_message(message.chat.id, text = answer.notification_answer_day(company))
                time.sleep(10)
        else: 
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id, text = "Уведомление выбрано")


    if reply == "2Дня":
        if answer.existence_of_polling == 0:
            answer.existence_of_polling = 1
            bot.delete_message(message.chat.id, message.id)
            while answer.existence_of_polling == 1:
                bot.send_message(message.chat.id, text = answer.notification_answer_2day(company))
                time.sleep(20)
        else:
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id, text = "Уведомление выбрано")


    if reply == "Неделя":
        if answer.existence_of_polling == 0:
            answer.existence_of_polling = 1
            bot.delete_message(message.chat.id, message.id)
            while answer.existence_of_polling == 1:
                bot.send_message(message.chat.id, text = answer.notification_answer_week(company))
                time.sleep(30)
        else:
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id, text = "Уведомление выбрано")

    if message.text == "О":
        print("j")
        answer.existence_of_polling = 0
    

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Подсоеденен пользователь, {message.from_user.first_name}')


if __name__ == '__main__':
    bot.infinity_polling()