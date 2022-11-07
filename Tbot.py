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

engine = create_engine('sqlite:///players.db')
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
    # message.reply("Привет", reply_markup=keyboard)
    # keyboard.add(key_bns, key_baw).add(key_show)
    # bot.edit_message_reply_markup(message.chat.id, message.message_id, 'Выбери:', reply_markup=keyboard)
    # bot.send_message(message.from_user.id, "Ваш текст", reply_markup=keyboard)

    # kb = [
    #     [
    #         types.KeyboardButton(text="Указать/Изменить имя и фамилию"),
    #         types.KeyboardButton(text="Указать/Изменить желание"),
    #         types.KeyboardButton(text="Показать моё имя и желание")
    #     ],
    # ]
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    # message.reply(reply_markup=keyboard)

    if message.text == 'Указать/Изменить имя и фамилию':
        bot.send_message(message.from_user.id, "Введи свои имя и фамилию")
        bot.register_next_step_handler(message, get_NameAndSurname)
        # get_NameAndSurname(message)
    elif message.text == 'Указать/Изменить желание':
        bot.send_message(message.from_user.id, "Введи своё желание")
        bot.register_next_step_handler(message, get_wish)
        # get_wish(message)
    elif message.text == 'Показать моё имя и желание':
        # bot.register_next_step_handler(message, show_wish_name)
        show_wish_name(message)

    # if message.text == "/start" or message.text == "/reg":
    #     bot.send_message(message.from_user.id, "Привет, введи свои имя и фамилию")
    #     bot.register_next_step_handler(message, get_NameAndSurname)
    # elif message.text == "/help":
    #     bot.send_message(message.from_user.id, "Введи имя и фамилию, после чего укажи пожелания для подарка")
    # else:
    #     bot.send_message(message.from_user.id, "Излишняя информация")


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

    # ns = message.text
    # keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    # key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    # keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    # key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    # keyboard.add(key_no);
    # question = 'Тебя зовут ' + str(ns) + '?';
    # bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    # ns = bot.register_next_step_handler(message, get_surnme)

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


# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
#         bot.send_message(call.message.chat.id, 'Запомню : )');
#     elif call.data == "no":
#         bot.send_message(call.message.from_user.id, "Привет, введи свои имя и фамилию")
#         bot.register_next_step_handler(call.message, get_NameAndSurname)


bot.polling(none_stop=True, interval=0)
