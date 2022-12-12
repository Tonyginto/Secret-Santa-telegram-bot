import datetime
import telebot
import updater
from telebot import types

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import table, column, select
import pandas as pd
# импортируем класс Players из файла AlSQL.py
from AlSQL import Players

engine = create_engine('sqlite:///players.db', connect_args={'check_same_thread': False})
# Свяжем engine с метаданными класса Players,
# чтобы декларативы могли получить доступ через экземпляр DBSession
Players.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# Экземпляр DBSession() отвечает за все обращения к базе данных
# и представляет «промежуточную зону» для всех объектов,
# загруженных в объект сессии базы данных.
session = DBSession()

file = open('botid.txt', 'r')
bot = telebot.TeleBot(file.read())
file.close()
commands = ['/help', '/insname', '/inswish', '/showmywish', '/showrecwish', '/']

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    dic = {'Указать/Изменить имя и фамилию':"Введи свои имя и фамилию",
           'Указать/Изменить желание':"Введи своё желание",
           '/insname':"Введи свои имя и фамилию",
           '/inswish':"Введи своё желание"}
    # key_bns = types.KeyboardButton(text='Указать/Изменить имя и фамилию')
    # key_baw = types.KeyboardButton(text='Указать/Изменить желание')
    # key_show = types.KeyboardButton(text='Моё имя и желание')
    # key_showrec = types.KeyboardButton(text='Имя и желание одаряемого')
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(key_bns,key_baw).row(key_show, key_showrec)
    if message.text in dic:
        pol = 1
        #bot.send_message(message.from_user.id, dic[message.text], reply_markup=keyboard)

    if message.text == 'Указать/Изменить имя и фамилию' or message.text.lower() == '/insname':
        #bot.send_message(message.from_user.id, "Введи свои имя и фамилию", reply_markup=keyboard)
        bot.send_message(message.from_user.id, "Введи свои имя и фамилию")
        bot.register_next_step_handler(message, get_NameAndSurname)
    elif message.text == 'Указать/Изменить желание' or message.text.lower() == '/inswish':
        bot.send_message(message.from_user.id, "Введи своё желание")
        bot.register_next_step_handler(message, get_wish)
    elif message.text == 'Моё имя и желание' or message.text.lower() == '/showmywish':
        show_wish_name(message.from_user.id)
    elif message.text == 'Имя и желание одаряемого' or message.text.lower() == '/showrecwish':
        show_gift_recepient(message.from_user.id)
    elif message.text.lower() == '/help' or message.text.lower() == '/start':
        bot.send_message(message.from_user.id, "Введи 'Указать/Изменить имя и фамилию'(/insname) или "
                                               "'Указать/Изменить желание'(/inswish) или "
                                               "'Моё имя и желание'(/showmywish) или "
                                               "'Имя и желание одаряемого'(/showrecwish)")
    else:
        bot.send_message(message.from_user.id, "Введи 'Указать/Изменить имя и фамилию'(/insname) или "
                                               "'Указать/Изменить желание'(/inswish) или "
                                               "'Моё имя и желание'(/showmywish) или "
                                               "'Имя и желание одаряемого'(/showrecwish)")
        # bot.send_message(message.from_user.id, "Введи /help")

def get_NameAndSurname(message):
    if message.text.lower() not in commands and message.text.lower()[0] != "/":
        try:
            player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
            player.name_surname = message.text
            session.add(player)
            session.commit()
        except:
            playerone = Players(id_telegram=message.from_user.id, name_surname=message.text, wish="", is_choose=False)
            session.add(playerone)
            session.commit()
        out_txt = "Изменено"
    else:
        out_txt = "Введённое имя представляет собой команду, некорректно, попробуй снова"
        bot.register_next_step_handler(message, get_NameAndSurname)
    bot.send_message(message.from_user.id, out_txt)

def get_wish(message):
    if message.text.lower() not in commands:
        player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
        player.wish = message.text
        player.last_change_wish = datetime.datetime.now()
        session.add(player)
        session.commit()
        out_txt = "Изменено"
    else:
        out_txt = "Введённое желание представляет собой команду, некорректно, попробуй снова"
        bot.register_next_step_handler(message, get_wish)
    bot.send_message(message.from_user.id, out_txt)

def show_wish_name(user_id):
    player = session.query(Players).filter_by(id_telegram=user_id).one()
    out_txt = "Имя: "+str(player.name_surname) + "\nЖелание: " + str(player.wish) if player != [] else "Сначала укажите своё имя и желание"
    bot.send_message(user_id, out_txt)

def show_gift_recepient(user_id):
    poles = session.query(Players).filter_by(id_telegram=user_id).one()
    id_rec = poles.choose_id
    if id_rec != None:
        recepient = session.query(Players).filter_by(id_telegram=id_rec).one()
        out_txt = "Задача оформить подарок для "+str(recepient.name_surname) + "\nЕго\\Её желание: " + str(recepient.wish)
        poles.last_check_wish = datetime.datetime.now()
        session.add(poles)
        session.commit()
    else:
        out_txt = "Одаряемый ещё не объявился"
    bot.send_message(user_id, out_txt)

# Здесь используется модуль telegram, ссылочка на habr: https://habr.com/ru/post/316666/
# j = updater.job_queue
#
# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
#
# j.run_repeating(start, interval=60, first=0)
# updater.start_polling()

# def check_wish_changing_rec(user_id):
#     player = session.query(Players).filter_by(id_telegram=user_id).one()
#     id_rec = session.query(Players).filter_by(id_telegram=player.choose_id).one()
#     if id_rec.last_change_wish > player.last_check_wish:
#         bot.send_message(player.id_telegram, "Получатель изменил желание")
#         show_gift_recepient(player.id_telegram)

def main():
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)
            print(datetime.datetime.now())

if __name__ == "__main__":
    main()