import telebot
from config import keys, TOKEN
from exceptions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def main(message: telebot.types.Message):
    text = 'Привет! Я Бот для отслеживания курса валют.'\
           '\n Для начала работы введите команду в следующем формате (через пробел):'\
           '\n- <Название валюты, цену которой Вы хотите узнать> '\
           '\n- <Название валюты, в которой Вы хотите узнать цену первой валюты> '\
           '\n- <Количество первой валюты> ' \
           '\n- Например, чтобы узнать цену 10 долларов в евро следует ввести '\
           '\n доллар евро 10 ' \
           '\n Список доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Что-то пошло не так :( \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
