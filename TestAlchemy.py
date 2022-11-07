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


# playerone = Players(id_telegram=1, name_surname="Антон Клягин", wish="мятная", is_choose=False)
# session.add(playerone)
# session.commit()

player = session.query(Players).filter_by(id_telegram=351637638).one()
out_txt = "Имя: " + str(player.name_surname) + "\nЖелание: " + str(player.wish)
print(out_txt)

# player = session.query(Players).filter_by(id_telegram=1).one()
# print(player.id)
# player.name_surname = "Аa"
# session.add(player)
# session.commit()

# bookToDelete = session.query(Players).filter_by(id_telegram=1).first()
# session.delete(bookToDelete)
# session.commit()

df = pd.read_sql_table('players', engine)
print(df)
# print(session.query(Players).sellect(id=1).all())


# t = table('players')
# s = select(t).where(t.c.id == 1)
# print(s)
# print(t.c)

# for user in session.query(Players).filter_by(id=1):
#      print(user)

# print(session.execute(select(t)).first()[0])
# print(s)