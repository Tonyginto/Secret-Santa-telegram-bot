import sys
# для настройки баз данных
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для создания отношений между таблицами
from sqlalchemy.orm import relationship

# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()

# здесь добавим классы
class Players(Base):
    __tablename__ = 'players'

    id = Column('id', Integer, primary_key=True)
    id_telegram = Column('id_telegram', Integer, nullable=False, unique=True)
    name_surname = Column('name_surname', String(250), nullable=False)
    wish = Column('wish', String(1000))
    is_choose = Column('is_choose', Boolean)
    choose_id = Column('choose_id', Integer)
    last_check_wish = Column('last_check_wish', DateTime)
    last_change_wish = Column('last_change_wish', DateTime)

# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///players.db')

Players.metadata.create_all(engine)