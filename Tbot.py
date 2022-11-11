import datetime
import telebot
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

bot = telebot.TeleBot('5601403756:AAEyQu-Y8wfoB39MCOiAZrfaoj5XquNG4oQ')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # наша клавиатура
    key_bns = types.KeyboardButton(text='Указать/Изменить имя и фамилию')
    key_baw = types.KeyboardButton(text='Указать/Изменить желание')
    key_show = types.KeyboardButton(text='Показать моё имя и желание')
    key_showrec = types.KeyboardButton(text='Показать имя и желание одаряемого')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(key_bns,key_baw).row(key_show, key_showrec)
    # bot.send_message(message.from_user.id, "Ваш текст", reply_markup=keyboard)

    if message.text == 'Указать/Изменить имя и фамилию' or message.text == '/insname':
        bot.send_message(message.from_user.id, "Введи свои имя и фамилию")
        bot.register_next_step_handler(message, get_NameAndSurname)
    elif message.text == 'Указать/Изменить желание' or message.text == '/inswish':
        bot.send_message(message.from_user.id, "Введи своё желание")
        bot.register_next_step_handler(message, get_wish)
    elif message.text == 'Показать моё имя и желание' or message.text == '/showmywish':
        show_wish_name(message)
    elif message.text == 'Показать имя и желание одаряемого' or message.text == '/showrecwish':
        show_gift_recepient(message)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Введи 'Указать/Изменить имя и фамилию'(/insname) или "
                                               "'Указать/Изменить желание'(/inswish) или "
                                               "'Показать моё имя и желание'(/showmywish) или "
                                               "'Показать имя и желание одаряемого'(/showmywish )")
    else:
        bot.send_message(message.from_user.id, "Введи /help")

def get_NameAndSurname(message):
    # player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
    # if player == []:
    #     playerone = Players(id_telegram=message.from_user.id, name_surname=message.text, wish="", is_choose=False)
    #     session.add(playerone)
    #     session.commit()
    # else:
    #     player.name_surname = message.text
    #     session.add(player)
    #     session.commit()
    try:
        player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
        player.name_surname = message.text
        session.add(player)
        session.commit()
    except:
        playerone = Players(id_telegram=message.from_user.id, name_surname=message.text, wish="", is_choose=False)
        session.add(playerone)
        session.commit()
    bot.send_message(message.from_user.id, "Изменено")

def get_wish(message):
    player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
    player.wish = message.text
    session.add(player)
    session.commit()
    bot.send_message(message.from_user.id, "Изменено")

def show_wish_name(message):
    player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
    out_txt = "Имя: "+str(player.name_surname) + "\nЖелание: " + str(player.wish) if player != [] else "Сначала укажите своё имя и желание"
    bot.send_message(message.from_user.id, out_txt)

def show_gift_recepient(message):
    id_rec = session.query(Players).filter_by(id_telegram=message.from_user.id).one().choose_id
    if id_rec != None:
        recepient = session.query(Players).filter_by(id_telegram=id_rec).one()
        out_txt = "Задача оформить подарок для "+str(recepient.name_surname) + "\nЕго желание: " + str(recepient.wish)
    else:
        out_txt = "Одаряемый ещё не объявился"
    bot.send_message(message.from_user.id, out_txt)

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        print(datetime.datetime.now())