import os
import telebot
# from keyboa import keyboa_maker
from telebot import types

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import table, column, select
import pandas as pd
# импортируем классы Players из файла AlSQL.py
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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(key_bns,key_baw).row(key_show)

    if message.text == 'Указать/Изменить имя и фамилию':
        bot.send_message(message.from_user.id, "Введи свои имя и фамилию")
        bot.register_next_step_handler(message, get_NameAndSurname)
    elif message.text == 'Указать/Изменить желание':
        bot.send_message(message.from_user.id, "Введи своё желание")
        bot.register_next_step_handler(message, get_wish)
    elif message.text == 'Показать моё имя и желание':
        show_wish_name(message)


def get_NameAndSurname(message):
    player = session.query(Players).filter_by(id_telegram=message.from_user.id).one()
    if player == []:
        playerone = Players(id_telegram=message.from_user.id, name_surname=message.text, wish="", is_choose=False)
        session.add(playerone)
        session.commit()
    else:
        player.name_surname = message.text
        session.add(player)
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
    out_txt = "Имя: "+str(player.name_surname) + "\nЖелание: " + str(player.wish)
    bot.send_message(message.from_user.id, out_txt)


bot.polling(none_stop=True, interval=0)
