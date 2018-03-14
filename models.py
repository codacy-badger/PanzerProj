from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

# create engine and connect do DB
connect_engine = create_engine('postgresql://fit_user:veryhardpass@localhost:5432/fit_db')
connection = connect_engine.connect()

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    def __repr__(self):
        return "<User(id='%s', username='%s', email='%s', first_name='%s', last_name='%s')>" \
               % (self.id, self.username, self.email, self.first_name, self.last_name)

# создание сессии
session = sessionmaker()
session.configure(bind=connect_engine)

Base.metadata.create_all(connect_engine)

