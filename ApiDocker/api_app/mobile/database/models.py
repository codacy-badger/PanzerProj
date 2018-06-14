from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# автоматический сбор инфомрации о таблицах в БД
Base = automap_base()

# подключаемся к БД
engine = create_engine('postgresql://fitness_admin:veryhardpass@localhost:5432/fitness_db')

# получаем схему таблиц в БД
Base.prepare(engine, reflect=True)

# получаем структуры конеретных таблиц из БД
auth_group = Base.classes.auth_group
auth_user = Base.classes.auth_user

# создаём сессию для работы
session = Session(engine)
