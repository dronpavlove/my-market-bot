"""
Основной модуль программы телеграмм-бота.
Содержит функции, отвечающие за взаимодействие бота с пользователем:
обработка команд;
обработка любых сообщений;
обработка нажатия кнопки.
"""

import telebot
from user_class import User, translate_eng
from typing import Any
from settings import TOKEN
import time
import json


users = dict()
bot = telebot.TeleBot(TOKEN)
command = ['help', 'Help', 'Shops', 'shops', 'Products', 'products', 'start', 'Start', 'Category', 'category']
command_text = '/shops — <i>список магазинов</i>' \
               '\n/products — <i>список товаров</i>'\
               '\n/category - <i>список категорий товаров</i>'


@bot.message_handler(commands=command)
def handle_command(message):
    """
    Обрабатывает команды типа '/text'
    """
    users[f"{message.chat.id}"] = [message.from_user.first_name, message.from_user.last_name]
    if message.text == '/help' or message.text == '/Help' or message.text == '/start' or message.text == '/Start':
        bot.send_message(message.chat.id, 'Выбирайте, что будем искать.\n'
                                          'Вот перечень моих команд:\n(Here is a list of my commands:)\n'
                         + command_text, parse_mode='HTML')

    elif message.text == '/Shops' or message.text == '/shops':
        User(message.chat.id, bot, command_text).shop_list(message)
    elif message.text == '/Category' or message.text == '/category':
        User(message.chat.id, bot, command_text).category_list(message)
    elif message.text == '/Products' or message.text == '/products':
        User(message.chat.id, bot, command_text).product_list(message)


@bot.message_handler(content_types=['text'])
def send_welcome(message):
    """
    Отвечает на текстовые сообщения, которые не предусмотрены в работе бота
    """
    text = translate_eng(message.text, 'Что-то пошло не так...'
                         '\nДавайте попробуем ещё раз.\nВот перечень моих команд:')
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, command_text, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def handle(call) -> Any:
    """
    Обработка кнопок.
    """
    if call.data.split(',')[0] == 'shop':
        my_shop_id = call.data.split(',')[1]
        User(call.message.chat.id, bot, command_text).shop_detail(call.message, my_shop_id)
    elif call.data.split(',')[0] == 'category':
        my_category_id = call.data.split(',')[1]
        User(call.message.chat.id, bot, command_text).category_detail(call.message, my_category_id)
    elif call.data.split(',')[0] == 'product':
        my_product_id = call.data.split(',')[1]
        print('вот продукт_id', my_product_id)
        User(call.message.chat.id, bot, command_text).product_detail(call.message, my_product_id)


while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)
