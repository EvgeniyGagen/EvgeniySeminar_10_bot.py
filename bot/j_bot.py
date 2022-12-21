import telebot 
import datetime as dt

from spy import *
# from telebot import types

bot = telebot.TeleBot("TOKEN", parse_mode=None)

print('start server')

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    log(message)
    if message.text == '/start':
      bot.reply_to(message, f'Привет, {message.from_user.first_name}.')
    elif message.text == '/help':
        bot.reply_to(message, f'Привет, {message.from_user.first_name}.\nЯ помогу тебе узнать сколько дней осталось до нового года.\nНапечатай /days.')
    
    

@bot.message_handler(content_types=["text"])
def send_welcome(message):
    log(message)
    if message.text == '/days':
        current_date = dt.datetime.now()
        new_year = dt.datetime(current_date.year +1,1,1)
        res = (new_year - current_date).days
        bot.reply_to(message, f'До нового года осталось {res} дней.')
        bot.send_photo(message.chat.id, 'https://images.wallpaperscraft.ru/image/single/novyy_god_prazdnik_elka_snezhinka_elochnye_igrushki_krupnyy_plan_36373_2560x1600.jpg')

bot.infinity_polling()    