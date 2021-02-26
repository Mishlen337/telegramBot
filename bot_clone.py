import config_clone
import Keyboards
import telebot
import check_answers
import time
import finance

bot = telebot.TeleBot(config_clone.token)
answer = check_answers.Answers()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Подсоеденен пользователь, {message.from_user.first_name}')

@bot.message_handler(commands=['set'])
def generate_markup(message):
    objMarkup = Keyboards.CostomizeKeyboard()
    markup = objMarkup.generate_primary_markup()
    bot.send_message(message.chat.id,'Выберите функции',reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def send_hi_messages(message):

    if message.text == 'Hi':
        bot.reply_to(message,f'Hello, {message.from_user.first_name}')

    elif message.text in config_clone.PRIMARYKEYBOARD:
        markup, text = answer.check_primary_answer(message.text)
        bot.send_message(message.chat.id, text = text,reply_markup = markup)     
       
    elif message.text in config_clone.THEORYKEYBOARD:
        bot.reply_to(message, answer.check_theory_answer(message.text))
    
    elif message.text in config_clone.QUOTEKEYBOARD:
        bot.reply_to(message, "Введите название компании ")

    elif message.text == config_clone.NOTIFICATIONKEYBOARD[0]:
        answer.existence_of_polling = 1
        while answer.existence_of_polling == 1:
            bot.reply_to(message, answer.check_notification_answer(message.text))
            time.sleep(20)
    
    elif message.text == 'Перестать посылать уведомления':
        answer.existence_of_polling = 0
    
    else:
        bot.send_message(message.chat.id,answer.check_quote_answer(message.text))


if __name__ == '__main__':
    bot.infinity_polling()