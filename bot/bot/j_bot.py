import telebot 
import time
from spy import *
from telebot import types

bot = telebot.TeleBot("TOKEN", parse_mode=None)

print('start server')

markup = types.ReplyKeyboardMarkup()                 # создаётся клавиатура
itembtn1 = types.KeyboardButton('котик')             # создаются кнопки
itembtn2 = types.KeyboardButton('ИМТ')  
markup.add(itembtn1, itembtn2)

@bot.message_handler(commands=['start','hello','help','info','cat'])
def send_welcome(message):
    log(message)
    if message.text == '/start':
	    bot.reply_to(message, f'Привет, {message.from_user.first_name}.')
    elif message.text == '/hello':
        bot.reply_to(message, f'Привет, {message.from_user.first_name}.\nЯ помогу тебе рассчитать индекс массы тела (ИМТ).\nЕсли готов(а), напиши что-нибудь.')
    elif message.text == '/help':     
        bot.reply_to(message, f'Для выбора команды начни вводить: /\nДля работы с ботом можно ввести любой текст.')
    elif message.text == '/info':     
        bot.reply_to(message, f'Что такое ИМТ?\nИндекс массы тела определяется как масса тела, поделенная на рост в квадрате.\nВаш ИМТ не всегда может давать точное представление о вашем здоровье, потому что он не учитывает соотношение жировой и мышечной массы тела.')    
    elif message.text == '/cat':  
        bot.reply_to(message, f'Хочешь посмотреть на котиков?\nПришли слово: котик')

@bot.message_handler(content_types=["text"])
def height_user(message):
    log(message)
    if message.text == 'котик':                        # пришлёт котика
        r = (f'https://cataas.com/cat?t=${time.time()}')
        bot.send_photo(message.chat.id, r, reply_markup=markup)    
    else:
        sent_msg = bot.send_message(message.chat.id, 'Укажите свой рост.')
        bot.register_next_step_handler(sent_msg, height_handler) 
          
def height_handler(message):
    log(message)
    height = float(message.text)
    sent_msg = bot.send_message(message.chat.id, f'Ваш рост {height}.\nА какой вес?')
    bot.register_next_step_handler(sent_msg, weight_handler, height)

def weight_handler(message, height):
    log(message)
    weight = float(message.text)
    res = round(weight/(height/100)**2,2)
    bot.send_message(message.chat.id, f'ИМТ = {res}.')
    if res > 30.0:
        bot.send_message(message.chat.id, f'У Вас ожирение. Хватит жрать.')
        bot.send_photo(message.chat.id, 'https://funart.pro/uploads/posts/2021-07/1625701332_10-funart-pro-p-tolstii-kot-zhivotnie-krasivo-foto-12.jpg')
    elif (res < 30.0 and res > 25.0):
        bot.send_message(message.chat.id, f'Показатель выше нормы.')
        bot.send_photo(message.chat.id, 'https://i.imgflip.com/2k2e10.jpg')
    elif (res < 25.0 and res > 18.5):
        bot.send_message(message.chat.id, f'Вы в прекрасной форме!')
        bot.send_photo(message.chat.id, 'https://avatars.mds.yandex.net/i?id=72d13c4adce78e8cbb7e204cd50830e9_l-5390142-images-thumbs&ref=rim&n=13&w=1078&h=1078')
    elif res < 18.5:
        bot.send_message(message.chat.id, f'Вам пора поесть.') 
        bot.send_photo(message.chat.id, 'https://adonius.club/uploads/posts/2022-06/1654457574_9-adonius-club-p-golodnii-kotik-krasivo-foto-9.jpg')   

bot.infinity_polling()    