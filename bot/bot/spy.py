import telebot

def log(message):
    data = open('user_message.txt', 'a+', encoding='utf-8')
    data.writelines(f'user_id: {message.from_user.id} текст: {message.text}\n')
    data.close() 
