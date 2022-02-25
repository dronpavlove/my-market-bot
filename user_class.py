"""Модуль содержит класс User"""

from telebot import types
import json
import requests
import re


class User:
    """
    Класс, отвечающий за взаимодействие с отдельным пользователем.
    Пинимает id-пользователя, сгенерированного бота и текстовую конструкцию для ответов.
    """
    def __init__(self, chat_id, bot, command_text):
        self.chat_id = chat_id
        self.bot = bot
        self.command_text = command_text

    def shop_list(self, message):
        text = translate_eng(message.text, "Веду поиск, надо подождать...")
        markup = types.InlineKeyboardMarkup()
        url = "http://pavloveav.beget.tech/api/shops/"
        response = requests.get(url)
        data_deaths = json.loads(response.text)
        for shop in data_deaths:
            button = types.InlineKeyboardButton(shop['name'], callback_data='shop, ' + str(shop['id']))
            markup.row(button)
        self.bot.send_message(self.chat_id, text, reply_markup=markup)

    def shop_detail(self, message, shop_id):
        text = translate_eng(message.text, "Веду поиск, надо подождать...")
        self.bot.send_message(self.chat_id, text)
        url = f"http://pavloveav.beget.tech/api/shops/{int(shop_id)}/"
        response = requests.get(url)
        shop = json.loads(response.text)
        text = '<b>' + str(shop['name']) + '</b>' + '\n<b>' + 'город: ' + '</b>' + \
               '<i>' + str(shop['city']) + '</i>' + \
               '\n<b>' + 'улица: ' + '</b>' + '<i>' + str(shop['street']) + '</i>' + \
               '\n<b>' + 'дом: ' + '</b>' + '<i>' + str(shop['house_number']) + '</i>' + \
               '\n<b>' + 'телефон: ' + '</b>' + '<i>' + str(shop['phone']) + '</i>' +\
               '\n<a href="' + str(shop['photo']) + '">' + 'фото' + '</a>'
        self.bot.send_message(self.chat_id, text, parse_mode='HTML')

    def category_list(self, message):
        text = translate_eng(message.text, "Веду поиск, надо подождать...")
        markup = types.InlineKeyboardMarkup()
        url = "http://pavloveav.beget.tech/api/category/"
        response = requests.get(url)
        data_deaths = json.loads(response.text)
        for category in data_deaths:
            button = types.InlineKeyboardButton(category['name'], callback_data='category,' + str(category['id']))
            markup.row(button)
        self.bot.send_message(self.chat_id, text, reply_markup=markup)

    def category_detail(self, message, category_id):
        text = translate_eng(message.text, "Веду поиск, надо подождать...")
        self.bot.send_message(self.chat_id, text)
        url = f"http://pavloveav.beget.tech/api/products/?category={int(category_id)}"
        response = requests.get(url)
        product_list = json.loads(response.text)
        for product in product_list:
            text = '<b>' + str(product['name']) + '</b>' + '\n<b>' + 'описание: ' + '</b>' + \
                   '<i>' + str(product['description']) + '</i>' + \
                   '\n<b>' + 'цена: ' + '</b>' + '<i>' + str(product['price']) + '</i>' + \
                   '\n<b>' + 'количество: ' + '</b>' + '<i>' + str(product['amount']) + '</i>' + \
                   '\n<a href="' + str(product['photo']) + '">' + 'фото' + '</a>'
            self.bot.send_message(self.chat_id, text, parse_mode='HTML')
            
    def product_list(self, message):
        text = translate_eng(message.text, "Веду поиск, надо подождать...")
        markup = types.InlineKeyboardMarkup()
        url = "http://pavloveav.beget.tech/api/products/"
        response = requests.get(url)
        data_deaths = json.loads(response.text)
        for product in data_deaths:
            button_text = str(product['name']) + str(product['price'])
            button = types.InlineKeyboardButton(button_text, callback_data='product, ' + str(product['id']))
            markup.row(button)
        self.bot.send_message(self.chat_id, text, reply_markup=markup)

    def product_detail(self, message, product_id):
        text = translate_eng(message.text, "Веду поиск, надо подождать...")
        self.bot.send_message(self.chat_id, text)
        url = f"http://pavloveav.beget.tech/api/products/"
        response = requests.get(url)
        product_list = json.loads(response.text)
        for product in product_list:
            if product['id'] == int(product_id[1::]):
                text = '<b>' + str(product['name']) + '</b>' + '\n<b>' + 'цена: ' + '</b>' + \
                       '<i>' + str(product['price']) + '</i>' + \
                       '\n<b>' + 'описание: ' + '</b>' + '<i>' + str(product['description']) + '</i>' + \
                       '\n<b>' + 'количество: ' + '</b>' + '<i>' + str(product['amount']) + '</i>' + \
                       '\n<a href="' + str(product['photo']) + '">' + 'фото' + '</a>'
        self.bot.send_message(self.chat_id, text, parse_mode='HTML')
            


def translate_eng(word, text):
    data_word = {
        "Если хотите продолжить, воспользуйтесь командами": "If you want to continue, use the commands",
        "Видимо, в этом городе нет известных нам отелей...": "Apparently, there are no hotels known to us in this city ...",
        "Веду поиск, надо подождать...": "Searching, gotta wait...",
        'Вводите цифрами, если десятичные- то с точкой: 12.32': 'Enter in numbers, if decimal- then with a dot: 12.32...',
        'Минимальная цена:': 'Minimum price:',
        'Максимальная цена:': 'Maximum price:',
        'Удалённость от центра:': 'Distance from the center:',
        "Выберите объект поиска:": "Select search object:",
        "Видимо проблемы с поиском. Попробуем ещё раз:": "Apparently there are problems with the search. Let's try again:",
        "Адрес: ": "Address: ",
        "стоимость: ": "price: ",
        "класс: ": "stars: ",
        "фото": "foto",
        "удалённость: ": "remoteness: ",
        'Какое количество отелей вывести?': 'How many hotels should you withdraw?',
        'Что-то пошло не так...\nДавайте попробуем ещё раз.\nВот перечень моих команд:':
            'Something went wrong...\nLet"s try again.\nHere is a list of my commands:'
    }
    leng = word.split(' ')[-1][0]
    if not re.search(r'[А-Яа-я]', leng):
        try:
            text = data_word[text]
        except:
            pass
    return text

