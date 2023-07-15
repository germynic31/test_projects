import telebot
import config
import random
from datetime import datetime
import pytz
from telebot import types
import time
from random import randint

bot = telebot.TeleBot(config.TOKEN)


# welcome
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Случайное число от 0 до 100")
    item2 = types.KeyboardButton("Как дела?")
    item3 = types.KeyboardButton("Какое сейчас время?")
    item4 = types.KeyboardButton("Правда или ложь?")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, крутой, но бесполезный бот.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


# commands and buttons
@bot.message_handler(content_types=['text'])
def buttons(message):
    if message.chat.type == 'private':
        if message.text == 'Случайное число от 0 до 100':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Норм", callback_data='good')
            item2 = types.InlineKeyboardButton("Все плохо", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Норм, ты как?', reply_markup=markup)
        elif message.text == 'Какое сейчас время?':
            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
            bot.send_message(message.chat.id, 'Время по мск: ' + str(moscow_time.strftime('%H:%M')))
        elif message.text == 'Правда или ложь?':
            randomnumber = randint(1, 2)
            if randomnumber == 1:
                bot.send_message(message.chat.id, 'Правда')
            elif randomnumber == 2:
                bot.send_message(message.chat.id, 'Ложь')

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить((')


# button "Как дела?"
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и хорошо')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Ну лан')

            # edit message
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела?",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


# start
bot.polling(none_stop=True)
