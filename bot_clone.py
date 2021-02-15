import config_clone
import telebot

bot = telebot.TeleBot(config_clone.token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Подсоеденен пользователь, {message.from_user.first_name}')

    
@bot.message_handler(content_types = ['text'])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.infinity_polling()

