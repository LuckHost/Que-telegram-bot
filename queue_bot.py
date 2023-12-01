import telebot
from telebot import types

bot = telebot.TeleBot('6286746396:AAH9saosXCHtGJcwZ74LGMEcLk32EcWHcYU')

def adding():
    print("купи арбуз")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    inf_button = types.KeyboardButton("Инфа")
    vvpd_button = types.KeyboardButton("ВВПДэ")
    op_button = types.KeyboardButton("ОПэ")
    
    markup.add(types.InlineKeyboardButton("Инфа", url="https://vk.com"))
    bot.send_message(message.from_user.id, "Опа", reply_markup=markup)
 

 
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
        

        
        
bot.infinity_polling()