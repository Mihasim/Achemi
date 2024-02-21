from config import settings

import telebot

from telegram.commands import TelegramInterface

bot = telebot.TeleBot(settings.TELEGRAM_API_KEI)

tag = ""
max_difficult = 0
min_difficult = None
name = ""
interface = TelegramInterface()
tasks = []


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/tag":
        bot.send_message(message.from_user.id, 'Введите tag по которому искать задачи')
        bot.register_next_step_handler(message, get_from_tag)
    elif message.text == "/name":
        bot.send_message(message.from_user.id, 'Введите название по которому искать задачи')
        bot.register_next_step_handler(message, get_from_name)
    else:
        bot.send_message(message.from_user.id, "Чтобы получить задачи по тегу и сложности введите /tag\n"
                                               "Чтобы получить информацию о задаче по названию введите /name")


def get_from_tag(message):
    global tag
    tag = message.text
    bot.send_message(message.from_user.id, 'Введите максимальный уровень сложности')
    bot.register_next_step_handler(message, get_max_difficult)


def get_max_difficult(message):
    global max_difficult
    while max_difficult == 0:
        try:
            max_difficult = int(message.text)
            if max_difficult < 0:
                bot.send_message(message.from_user.id, 'Число должно быть положительным')
                max_difficult = 0
        except Exception:
            max_difficult = 0
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

    bot.send_message(message.from_user.id, 'Введите минимальный уровень сложности')
    bot.register_next_step_handler(message, get_min_difficult)


def get_min_difficult(message):
    global min_difficult, tasks
    while min_difficult is None:
        try:
            min_difficult = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    tasks = interface.search_for_tag(tag, min_difficult, max_difficult)
    for task in tasks:
        bot.send_message(message.from_user.id, f'{task}')


def get_from_name(message):
    global name
    name = message.text
    message_ = interface.search_for_name(name)
    bot.send_message(message.from_user.id, message_)


def start_bot():
    bot.polling(none_stop=True, interval=0)
start_bot()
