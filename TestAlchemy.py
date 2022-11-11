import random
import keyboa
from keyboa import keyboards
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import table, column, select
import pandas as pd
# импортируем классы Players и Base из файла AlSQL.py
from AlSQL import Players, Base

engine = create_engine('sqlite:///players.db')
# Свяжим engine с метаданными класса Base,
# чтобы декларативы могли получить доступ через экземпляр DBSession
Players.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# Экземпляр DBSession() отвечает за все обращения к базе данных
# и представляет «промежуточную зону» для всех объектов,
# загруженных в объект сессии базы данных.
session = DBSession()


# playerone = Players(id_telegram=3, name_surname="asdsdasddd", wish="мятная", is_choose=False)
# session.add(playerone)
# session.commit()

# player = session.query(Players).filter_by(id_telegram=1).one()
# print(player.id)
# player.name_surname = "Аa"
# session.add(player)
# session.commit()

# bookToDelete = session.query(Players).filter_by(id=2).first()
# session.delete(bookToDelete)
# session.commit()

# print(session.query(Players).sellect(id=1).all())


# t = table('players')
# s = select(t).where(t.c.id == 1)
# print(s)
# print(t.c)

# for user in session.query(Players).filter_by(id=1):
#      print(user)

# print(session.execute(select(t)).first()[0])
# print(s)

def randoming_players():
    all_play = session.query(Players).filter_by(is_choose=False).all()
    num = len(all_play)
    l, f = list(range(0, num)), False
    while not f:
        random.shuffle(l)
        f = [False if i == l[i] else True for i in range(num)]
        f = True if all(f) else False
        # i: int = 0
        # while i < num:
        #     if i == l[i]:
        #         random.shuffle(l)
        #         break
        #     i += 1
        # if i == num: f = True
    for i in range(num):
        all_play[i].choose_id, all_play[i].is_choose = all_play[l[i]].id_telegram , True
        session.add(all_play[i])
        session.commit()

def allFalse():
    for i in session.query(Players).filter_by(is_choose=True).all():
        i.is_choose, i.choose_id = False, None
        session.add(i)
        session.commit()

allFalse()
randoming_players()
df = pd.read_sql_table('players', engine)
print(df)